from typing import Optional, Any, Union, List, Dict, Tuple

from drb import DrbItem
from drb.node import DrbNode
from drb.factory import DrbFactory, DrbSignature, DrbSignatureType
from drb.path import Path


class DrbMemNode(DrbNode):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace_uri(self) -> Optional[str]:
        return None

    @property
    def value(self) -> Optional[Any]:
        return None

    @property
    def path(self) -> Optional[Path]:
        return None

    @property
    def attributes(self) -> Dict[Tuple[str, str], DrbItem]:
        return {}

    def get_attribute(self, name: str, namespace_uri: str = None) -> \
            Optional[DrbItem]:
        pass

    @property
    def parent(self) -> Optional[DrbNode]:
        return None

    @property
    def children(self) -> List[DrbNode]:
        return []

    def has_child(self) -> bool:
        pass

    def insert_child(self, node: DrbNode, index: int) -> None:
        pass

    def append_child(self, node: DrbNode) -> None:
        pass

    def replace_child(self, index: int, new_node: DrbNode) -> None:
        pass

    def remove_child(self, index: int) -> None:
        pass

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        pass

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        pass

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type) -> Any:
        return None

    def close(self) -> None:
        pass

    def __len__(self):
        pass

    def __getitem__(self, item):
        pass

    def __truediv__(self, other):
        pass


class DrbMemFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        return DrbMemNode(f'Mem_{node.name}')


class MemSignature(DrbSignature):
    def __init__(self):
        self._factory = DrbMemFactory()

    @property
    def uuid(self) -> str:
        return '09d14890-283b-11ec-9621-0242ac130002'

    @property
    def label(self) -> str:
        return 'mem'

    @property
    def category(self) -> DrbSignatureType:
        return DrbSignatureType.PROTOCOL

    @property
    def factory(self) -> DrbFactory:
        return self._factory

    def match(self, node: DrbNode) -> bool:
        return 'mem' == node.path.scheme
