from __future__ import annotations

import abc
from typing import List, Union, Dict, Optional, Tuple, Any
from .item import DrbItem
from .node_impl import NodeImpl
from .path import ParsedPath
from .predicat import Predicate
from .exceptions import DrbException, DrbNotImplementationException

"""
    Generic node interface. This interface represents a single node of a tree
    of data. Any node can have no, one or several children. This interface
    provides the primarily operations to browse an entire data structure. All
    implementations of the "Data Request Broker" shall be able to produce such
    nodes.
"""


class DrbNode(DrbItem, NodeImpl, abc.ABC):
    @property
    @abc.abstractmethod
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        """ Returns attributes of the current node.
        This operation all attributes owned by the current node.
        Attributes are represented by a dict with as key the tuple
        (name, namespace_uri) of the attribute and as value the value of this
        attribute.
        :return: The a dict attributes of the current node.
        :rtype: dict
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        """
        Returns the value of the corresponding attribute, following it's name
        and it's namespace URI for the matching.
        :param name: attribute name to match.
        :type name: str
        :param namespace_uri: attribute namespace URI to match.
        :type namespace_uri: str
        :return: the associated value of the matched attribute.
        :rtype: Any
        :raises:
            DrbException: if the given name and namespace URI not math any
                          attribute of the current node.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def parent(self) -> Optional[DrbNode]:
        """
        The parent of this node. Returns a reference to the parent node of the
        current node according to the current implementation. Most of the
        nodes have a parent except root nodes or if they have just been
        removed, etc. If the node has no parent the operation returns None.
        :return: The parent of this node or None.
        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def path(self) -> ParsedPath:
        """ The full path of this node.
        The path it the complete location of this node. The supported format
        is URI and apache common VFS. Examples of path (

        """
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def children(self) -> List[DrbNode]:
        """
        The list of children of the current node. Returns a list of
        references to the children of the current node. The current node may
        have no child and the operation returns therefore a null reference.
        :return: The list of children if any null otherwise.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def has_child(self) -> bool:
        """
        Checks if current node is parent of at least one child.
        :return: true if current node has at least one child, false otherwise
        """
        raise NotImplementedError

    @abc.abstractmethod
    def insert_child(self, index: int, node: DrbNode) -> None:
        """
        Inserts a child at a given position. The passed node is inserted in
        the list of children at the given position The position is the
        expected index of the node after insertion. All the previous
        children from the aimed position to the end of the list are shift to
        the end of the new children list (i.e. their indices are shifted up
        of 1). If the given index is out of the children bounds and
        therefore less than zero and greater or equal to the current number
        of children,the operation raises an exception. An index equal to the
        current number of children is allowed and the
        operation is therefore equivalent to append_child().
        If the node has been inserted within the children list, the next
        sibling indices are increased of one. In addition the associations
        between the inserted node and it previous and next siblings are
        updated (if any).

        Important note: The implementation of the node is not supposed to
        accept any kind of node For instance it may not be possible to
        insert a node wrapping a file in an XML document. The documentation
        of the implementation shall describe its specific strategy.
        Case of unordered or specifically ordered implementations:</b> If
        the implementation does not support ordered children or has specific
        ordering rules, the node is inserted without taking into account the
        requested index passed in parameter. For instance it may not be
        possible to impose the file order in a directory: it generally
        depends on the lexicographical order of the node names or their
        creation date.

        Events: This operation fires a node change event when the
        implementation is a node change producer. The node affected by the
        change is the inserted node and the source is the current node. The
        called operation is the nodesInserted() of the listeners.
        :param: node A reference to the node to be inserted.
        :param: index The expected index of the node after the insertion.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def append_child(self, node: DrbNode) -> None:
        """
        Appends a child at the end of the children list. The passed node is
        inserted in the list of children at the end of the current list.

        Important note: The implementation of the node is not supposed to
        accept any kind of node For instance it may not be possible to
        append a node wrapping a file in an XML document. The documentation
        of the implementation shall describe its specific strategy.
        Case of unordered or specifically ordered implementations: If the
        implementation does not support ordered children or has specific
        ordering rules, the node may not be appended but only inserted
        according to these rules. For instance it may not be possible to
        impose the file order in a directory:it generally depends on the
        lexicographical order of the node names or their creation date.

        Events: This operation fires a node change event when the
        implementation is a node change producer. The node affected by the
        change is the appended node and the source is the current node. The
        called operation is the nodesInserted() of the listeners.
        :param: node A reference to the node to be appended.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def replace_child(self, index: int, new_node: DrbNode) -> None:
        """
        Replaces a child of the current node. This operation replaces a
        child in the current children list by a new one The operation aborts
        when the index is out of bound (index < 0 || index > size). In case
        of error, the implementation has to restore the initial situation.
        It is therefore recommended for any implementation to check the
        consistency prior to perform the replacement.

        Important note: The implementation of the node is not supposed to
        accept any kind of node For instance it may not be possible to
        insert a node wrapping a file in an XML document. The documentation
        of the implementation shall describe its specific strategy.

        Events: This operation fires a node change event when the
        implementation is a node change producer. The node affected by the
        change is the new node and the source is the current node. The
        called operation is the structure_changed() of the listeners.
        :param index: Index of the node to be replaced. This index starts at
        0 and shall be less than the number of children.
        :param new_node: A reference to the node that replaces the old one.
        :return: A reference to the effectively replacing node.This
        reference may differ from the new_node parameter.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_child(self, index: int) -> None:
        """
        Removes an existing child. The child at the given index is removed
        from the children list of the current node. The child is not
        modified by this operation. At the child point of view it keeps the
        same parent or any common association depending on the
        implementation. However at the parent (i.e. the current node) point
        of view the removed node is completely dismissed and will never be
        re-instantiated from constructor operations (e.g. get_first_child(),
        etc. ). The index of the child to be removed has to correspond to an
        existing children index. If the index is less than zero or greater
        or equal to the current number of children, an exception is  thrown.
        This operation takes into account the removal by updating the
        sibling associations of the children nodes prior and next to the
        removed one. The indices of the nodes next to the removed one are
        decreased of one. Their parents as well as their contents are left
        unchanged.

        Events: This operation fires a node change event when the
        implementation is a node change producer. The node affected by the
        change is the removed node and the source is the current node.The
        called operation is the nodesRemoved() of the listeners.
        :param index: Index of the child to be removed.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_attribute(self, name: str, value: Optional[Any] = None,
                      namespace_uri: Optional[str] = None) -> None:
        """
        Adds an attribute to the current node.
        :param name: attribute name
        :type name: str
        :param namespace_uri: attribute namespace URI
        :type namespace_uri: str
        :param value: attribute value
        :type value: Any
        :raises:
            DrbException: if the attribute already exists.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove_attribute(self, name: str, namespace_uri: str = None) -> None:
        """
        Removes the corresponding attribute.
        :param name: attribute name
        :type name: str
        :param namespace_uri: attribute namespace URI
        :type namespace_uri: str
        :raises:
            DrbException: if the attribute is not found.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        """
        Releases all resources attached to the current node.
        """
        raise NotImplementedError

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: int = None) -> Union[DrbNode,
                                                          List[DrbNode]]:
        """
        Retrieves a child with the given name, namespace and occurrence. Can
        also retrieves a list of child if the occurrence is not specified.

        :param name: child name
        :type name: str
        :param namespace_uri: child namespace URI (default: None)
        :type namespace_uri: str
        :param occurrence: child occurrence (default: None)
        :type occurrence: int
        :returns: the requested DrbNode if the occurrence is defined, otherwise
         a list of requested DrbNode children
        :rtype: DrbNode | List[DrbNode]
        """
        try:
            named_children = [x for x in self.children if x.name == name]
            if occurrence is None and len(named_children) > 0:
                # test on len avoid to return a empty list
                return named_children
            elif occurrence > 0:
                # test avoid to get the last element if occurrence is 0..
                return named_children[occurrence - 1]
            else:
                raise DrbException(f'Child ({name},{occurrence}) not found')
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child ({name},{occurrence}) not found') \
                from error

    def __len__(self):
        """len operator return the number of children.
        This len operator returns the children count.
        """
        if not self.children:
            return 0
        return len(self.children)

    def __getitem__(self, item):
        """Implements the item in brace operator to access this node children.
        The brace operator is used to access the children node, according to
        the following rules:

        - If item is a DrbNode, this node retrieved from this nodes children is
        returned. In case of multiple occurrence of the node, a list of nodes
        is returned.

        - If item is a single string, the children nodes with the item as name
        is retrieved from its children.

        - If item is a integer (int), the item-th children node will be
         returned.

         - If item is a tuple (name: str, namespace: str, occurrence: int)
              * item[0] shall be the children node name,
              * item[1] could be the namespace
              * item[2] could be the occurrence of the node.
            Namespace and occurrence are optional, node name is mandatory.
         The tuple retrieved the node occurrence.

         - If Item is subclass of Predicate, children nodes matching this
            predicate are returned.

        Except when using integer index, a list is always returned.
        When the item does not match any result, DrbNodeException is raised,
        except for predicate which is able to return empty child list.
        """
        if isinstance(item, DrbNode):
            children = self._get_named_child(name=item.name,
                                             namespace_uri=item.namespace_uri)
        elif isinstance(item, str):
            children = self._get_named_child(name=item)
        elif isinstance(item, int):
            try:
                children = self.children[item]
            except (TypeError, IndexError) as e:
                raise DrbException(
                    f"Not found children index {item} in {self.name}") from e
        elif isinstance(item, tuple):
            if len(item) == 1:
                children = self[item[0]]
            elif len(item) == 2:
                if isinstance(item[1], str):
                    children = self._get_named_child(name=item[0],
                                                     namespace_uri=item[1])
                elif isinstance(item[1], int):
                    children = self._get_named_child(name=item[0],
                                                     occurrence=item[1])
                else:
                    raise DrbException(
                        f"Wrong tuple type {type(item[1])}.")
            elif len(item) == 3:
                children = self._get_named_child(name=item[0],
                                                 namespace_uri=item[1],
                                                 occurrence=item[2])
            else:
                raise DrbException(f'Unknown tuple format {item}')
        elif isinstance(item, Predicate):
            children = []
            for c in self.children:
                if item.matches(c):
                    children.append(c)
        else:
            raise DrbNotImplementationException(
                f"{type(item)} type not managed.")
        return children

    def __truediv__(self, child):
        """Div operator setup to manage access to children list.
        The truediv operator is redefined here to manage path navigation as
        posix style representation. It allows access to the children by their
        names.
        The navigation behaviour depends on the right element of the div
        operator:
        - If the right operator is a string, operator results a list of
           children nodes matching this name string.
        - If the right operator is a DrbNode, operator results a list of
           children nodes matching this node name and namespace.
        - If the the right operator is subclass of class Predicate, operator
           results a list of children nodes matching the predicate
        """
        if isinstance(child, DrbNode):
            children = self._get_named_child(name=child.name,
                                             namespace_uri=child.namespace_uri)
        elif isinstance(child, str):
            children = self._get_named_child(name=child)
        elif isinstance(child, Predicate):
            children = []
            for c in self.children:
                if child.matches(c):
                    children.append(c)
        else:
            raise DrbNotImplementationException(
                f"{type(child)} type not managed.")
        return children
