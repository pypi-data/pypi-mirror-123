from typing import Optional, Any, Union, List, Dict, Tuple

from drb.node import DrbNode
from drb.path import Path, parse_path, ParsedPath
from drb.exceptions import DrbException
from drb.events import Event
from pathlib import PurePath

from deprecation import deprecated


class DrbLogicalNode(DrbNode):
    """Logical Node for Drb
    This node implements a in-memory logical node, It can be used as default
    node for virtual nodes hierarchy. It can also be used as a wrapper of
    the source node, in this case, the source node is clone.
        *parent* (DrbNode) - Used only if source is not a DrbNode
        *namespace_uri (str) - Used only if source is not a DrbNode
        *value* (any) - Used only if source is not a DrbNode
        **kwargs (dict) – Additional keyword arguments: For possible future use
    """
    def __init__(self, source: Union[DrbNode, str, Path, PurePath],
                 parent: DrbNode = None, namespace_uri: str = None,
                 value: any = None, **kwargs):
        self.changed = Event()
        self._wrapped_node = None
        # case of source is an url string
        if isinstance(source, (str, Path, PurePath)):
            self._path = None
            self._path_source = parse_path(source)
            self._name = self._path_source.filename
            self._namespace_uri = namespace_uri
            self._value = value
            self._attributes = None
            self._parent = parent
            self._children = None
        elif isinstance(source, DrbNode):
            self._wrapped_node = source

    @property
    def name(self) -> str:
        if self._wrapped_node is not None:
            return self._wrapped_node.name
        return self._name

    @property
    def namespace_uri(self) -> Optional[str]:
        if self._wrapped_node is not None:
            return self._wrapped_node.namespace_uri
        return self._namespace_uri

    @property
    def value(self) -> Optional[Any]:
        if self._wrapped_node is not None:
            return self._wrapped_node.value
        return self._value

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._wrapped_node is not None:
            return self._wrapped_node.attributes
        return self._attributes

    @property
    def parent(self) -> Optional[DrbNode]:
        if self._wrapped_node is not None:
            return self._wrapped_node.parent
        return self._parent

    @property
    def path(self) -> ParsedPath:
        if self._wrapped_node is not None:
            return self._wrapped_node.path
        if self._path is None:
            if self._path_source.absolute or self.parent is None:
                self._path = self._path_source
            else:
                self._path = self.parent.path / self._path_source
        return self._path

    @property
    def children(self) -> List[DrbNode]:
        if self._wrapped_node is not None:
            return self._wrapped_node.children
        return self._children

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type) -> Any:
        raise DrbException(
            f"Implementation for {impl.__name__} not supported.")

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        try:
            return self.attributes[(name, namespace_uri)]
        except (IndexError, TypeError, KeyError) as error:
            raise DrbException(f'No attribute {name} found') from error

    def has_child(self) -> bool:
        if not self.children:
            return False
        return len(self.children) > 0

    @deprecated(details="Use the brace with tuple: "
                        "node[name, namespace, occurrence]")
    def get_named_child(self, name: str, namespace_uri: str = None,
                        occurrence: int = None) -> Union[DrbNode,
                                                         List[DrbNode]]:
        return self._get_named_child(name=name,
                                     namespace_uri=namespace_uri,
                                     occurrence=occurrence)

    @deprecated(details="Use the brace with list index: node[0]")
    def get_first_child(self) -> Optional[DrbNode]:
        try:
            return self.children[0]
        except (IndexError, TypeError) as error:
            raise DrbException(f'First child not found') from error

    @deprecated(details="Use the brace with list index: node[-1]")
    def get_last_child(self) -> Optional[DrbNode]:
        try:
            return self.children[-1]
        except (IndexError, TypeError) as error:
            raise DrbException(f'Last child not found') from error

    @deprecated(details="Use the brace with list index: node[idx]")
    def get_child_at(self, index: int) -> DrbNode:
        try:
            return self.children[index]
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child index {index} not found') from error

    @deprecated(details="Use the len function : len(node)")
    def get_children_count(self) -> int:
        if not self.children:
            return 0
        return len(self.children)

    def _add_child_init(self, node: DrbNode):
        if self.children is None:
            self.children = []
        if node.parent != self:
            node.parent = self

    def insert_child(self, index: int, node: DrbNode) -> None:
        if self._wrapped_node is not None:
            self._wrapped_node.insert_child(index, node)
        else:
            self._add_child_init(node)
            self._children.insert(index, node)

    def append_child(self, node: DrbNode) -> None:
        if self._wrapped_node is not None:
            self._wrapped_node.append_child(node)
        else:
            self._add_child_init(node)
            self._children.append(node)

    def replace_child(self, index: int, new_node: DrbNode) -> None:
        try:
            if self._wrapped_node is not None:
                self._wrapped_node.replace_child(index, new_node)
            else:
                self._children[index] = new_node
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child index {index} not found') from error

    def remove_child(self, index: int) -> None:
        try:
            if self._wrapped_node is not None:
                self._wrapped_node.remove_child(index)
            else:
                del self._children[index]
        except (IndexError, TypeError, AttributeError) as error:
            raise DrbException(f'Child index {index} not found') from error

    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:

        if (name, namespace_uri) in self.attributes:
            raise DrbException(f'Attribute {name}' +
                               ',{namespace_uri}' if namespace_uri else '' +
                               ' already exists')
        self.attributes[(name, namespace_uri)] = value
        self.changed.notify(self, 'attributes', action='add', name=name)

    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        try:
            del self.attributes[(name, namespace_uri)]
        except (KeyError, TypeError) as error:
            raise DrbException(f'No attribute {name}'
                               ',{namespace_uri}' if namespace_uri else '' +
                                                                        'found'
                               ) from error
        self.changed.notify(self, 'attributes', action='remove', name=name)

    def close(self) -> None:
        """
        The wrapped not (if any) is not closed here: This class only wraps
        the values of given node. Nothing is to be closed here.
        """
        if self._wrapped_node is not None:
            return self._wrapped_node.close()

    def __str__(self):
        string = '<'
        if self.namespace_uri:
            string = string + f"{self.namespace_uri}:"
        string = string + f"{self.name}"
        if self.attributes:
            for name, namespace in self.attributes.keys():
                string = string + ' "'
                if namespace:
                    string = string + f'{namespace}:'
                string = string + f'{name}"="'
                string = \
                    string + f'{str(self.attributes.get((name, namespace)))}"'
        if self.value:
            string = string + f'>{str(self.value)}</{self.name}>'
        else:
            string = string + '/>'
        return string

    def __repr__(self):
        return self.__str__()

    @attributes.setter
    def attributes(self, value):
        if self._wrapped_node is not None:
            self._wrapped_node.attributes = value
        else:
            self._attributes = value
        self.changed.notify(self, 'attributes', value)

    @children.setter
    def children(self, value):
        if self._wrapped_node is not None:
            self._wrapped_node.children = value
        else:
            self._children = value
        self.changed.notify(self, 'children', value)

    @parent.setter
    def parent(self, value):
        if self._wrapped_node is not None:
            self._wrapped_node.parent = value
        else:
            self._parent = value
            self._path = None
        self.changed.notify(self, 'parent', value)

    @name.setter
    def name(self, value):
        if self._wrapped_node is not None:
            self._wrapped_node.name = value
        else:
            self._name = value
        self.changed.notify(self, 'name', value)

    @namespace_uri.setter
    def namespace_uri(self, value):
        if self._wrapped_node is not None:
            self._wrapped_node.namespace_uri = value
        else:
            self._namespace_uri = value
        self.changed.notify(self, 'namespace_uri', value)

    @value.setter
    def value(self, value):
        if self._wrapped_node is not None:
            self._wrapped_node.value = value
        else:
            self._value = value
        self.changed.notify(self, 'value', value)
