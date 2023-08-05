import importlib
import sys
import inspect
import logging
import abc
from enum import Enum, auto
from types import ModuleType
from typing import Callable, Dict, List, Optional, Type, Union
if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points
from importlib.metadata import EntryPoint

from .factory import DrbFactory
from .. import DrbNode
from ..exceptions import DrbFactoryException
from ..utils.logical_node import DrbLogicalNode


logger = logging.getLogger('DrbResolver')


class DrbSignatureType(Enum):
    SECURITY = auto(),
    PROTOCOL = auto(),
    CONTAINER = auto(),
    FORMATTING = auto()


class DrbSignature(abc.ABC):
    @property
    @abc.abstractmethod
    def uuid(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def label(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def category(self) -> DrbSignatureType:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def factory(self) -> DrbFactory:
        raise NotImplementedError

    @abc.abstractmethod
    def match(self, node: DrbNode) -> bool:
        raise NotImplementedError


class DrbFactoryResolver(DrbFactory):
    """ The factory resolver

    The factory resolver aims to parametrize the selection of the factory
    able to resolves the nodes according to its physical input.
    """

    __instance = None

    @classmethod
    def __inspect_class_filter(cls, module: ModuleType) -> Callable:
        """
        Generates a filter which allows to retrieve classes defined in the
        given module (without classes imported in this module)
        """
        return lambda m: inspect.isclass(m) and m.__module__ == module.__name__

    @classmethod
    def __load_signature(cls, entry: EntryPoint) -> DrbSignature:
        """
        Retrieves the signature node defined in the given entry point.
        :param entry: plugin entry point
        :type entry: EntryPoint plugin entry point
        :returns: the specific implemented factory
        :rtype: DrbSignature
        :raises:
            * DrbFactoryException If no DrbSignature is found.
        """
        try:
            module = importlib.import_module(entry.value)
        except ModuleNotFoundError:
            raise DrbFactoryException(f'Module not found: {entry.value}')

        is_class = cls.__inspect_class_filter(module)
        for name, obj in inspect.getmembers(module, is_class):
            if obj != DrbSignature and issubclass(obj, DrbSignature):
                return obj()
        raise DrbFactoryException(
            f'No DrbSignature found in module: {entry.value}')

    @classmethod
    def __load_drb_signatures(cls, drb_metadata: str) -> \
            Dict[str, DrbSignature]:
        """
        Loads all DRB plugin defined in the current environment
        :returns: A dict mapping factory names as key to the corresponding
            factory
        :rtype: dict
        """
        impls = {}
        plugins = entry_points(group=drb_metadata)

        if not plugins:
            logger.warning('No DRB plugin found')
            return impls

        for name in plugins.names:
            if name not in impls.keys():
                try:
                    signature = DrbFactoryResolver.__load_signature(
                        plugins[name])
                    impls[signature.uuid] = signature
                except DrbFactoryResolver:
                    message = f'Invalid DRB plugin: {name}'
                    logger.warning(message)
                    raise DrbFactoryException(message)
            else:
                logger.warning(f'DRB plugin already loaded: {name}')

        return impls

    def __init__(self):
        self.__signatures = self.__load_drb_signatures('drb.impl')
        self.__protocols = [s for k, s in self.__signatures.items()
                            if s.category == DrbSignatureType.PROTOCOL]
        self.__main_containers = self.__retrieve_main_containers(DrbSignature)
        self.__formats = [s for k, s in self.__signatures.items()
                          if s.category == DrbSignatureType.FORMATTING]

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DrbFactoryResolver, cls).__new__(cls)
        return cls.__instance

    def _create(self, node: DrbNode) -> DrbNode:
        return self.resolve(node).factory.create(node)

    def __retrieve_main_containers(self, cls: Type) -> List[DrbSignature]:
        """
        Retrieves the list of all container signature not having as parent
        class another than the given class.

        :returns: a list of container signature
        :rtype: list
        """
        containers = []
        for k, s in self.__signatures.items():
            if s.category == DrbSignatureType.CONTAINER and \
                    s.__class__ in cls.__subclasses__():
                containers.append(s)
        return containers

    def __retrieve_protocol(self, node: DrbNode) -> Optional[DrbSignature]:
        """
        Retrieves the protocol signature associated to the given node.

        :param node: node which need to be resolved
        :type node: DrbNode
        :returns: a protocol signature or None if no protocol signature match
            the given node
        :rtype: DrbSignature
        """
        for protocol in self.__protocols:
            if protocol.match(node):
                return protocol
        return None

    def __retrieve_container(self, node: DrbNode) -> Optional[DrbSignature]:
        """
        Retrieves the container signature associated to the given node.
        :param node: node which need to be resolved
        :type node: DrbNode
        :returns: a signature matching the given node, otherwise None
        :rtype: DrbSignature
        """
        for s in self.__main_containers:
            if s.match(node):
                return self.__finest_container(node, s)
        return None

    def __finest_container(self, node: DrbNode, finest: DrbSignature) \
            -> DrbSignature:
        """
        Retrieves the finest container signature associated to the given node.
        :param node: node which need to be resolved
        :type node: DrbNode
        :param finest: the current finest signature matching with the given
            node
        :type finest: DrbSignature
        :returns: a signature matching the given node
        :rtype: DrbSignature
        """
        signatures = self.__retrieve_main_containers(finest.__class__)
        for s in signatures:
            if s.match(node):
                return self.__finest_container(node, s)
        return finest

    def __retrieve_formatting(self, node) -> Optional[DrbSignature]:
        """
        Retrieves the formatting signature associated to the given node.

        :param node: node which need to be resolved
        :type node: DrbNode
        :returns: a signature matching the given node, otherwise None
        :rtype: DrbSignature
        """
        for s in self.__formats:
            if s.match(node):
                return s
        return None

    def resolve(self, source: Union[str, DrbNode]) -> DrbSignature:
        """Resolves the signature related to the passed source.

        :param source: source to be resolved
        :returns: the implemented factory
        :rtype: DrbSignature
        :raises:
            * DrbFactoryException when no factory matches this uri.
        """
        if isinstance(source, str):
            node = DrbLogicalNode(source)
        else:
            node = source
        protocol = self.__retrieve_protocol(node)
        if protocol is None:
            raise DrbFactoryException(f'Cannot resolve: {source}')
        node = protocol.factory.create(node)

        container = self.__retrieve_container(node)
        if container is None:
            signature = self.__retrieve_formatting(node)
            if signature is None:
                return protocol
            else:
                return signature
        return container
