import re
from typing import Optional, Any, Union, List, Dict, Tuple

import drb
from typing.io import IO
from xml.etree.ElementTree import parse, Element
from io import BufferedIOBase, RawIOBase

from drb import DrbNode
from drb.exceptions import DrbNotImplementationException, DrbException
from drb.utils.logical_node import DrbLogicalNode


def extract_namespace_name(value: str) -> Tuple[str, str]:
    """
    Extracts namespace and name from a tag of a Element
    :param value: XML element tag
    :type value: str
    :return: a tuple containing the extracted namespace and name
    :rtype: tuple
    """
    ns, name = re.match(r'({.*})?(.*)', value).groups()
    if ns is not None:
        ns = ns[1:-1]
    return ns, name


class XmlNode(DrbLogicalNode):

    def __init__(self, element: Element, parent: DrbNode = None):
        namespace_uri, name = extract_namespace_name(element.tag)
        DrbLogicalNode.__init__(self, name, parent=parent,
                                namespace_uri=namespace_uri)
        self._elem: Element = element
        self._path = None

    @property
    def value(self) -> Optional[Any]:
        if self.has_child():
            return None
        return self._elem.text

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attributes is None:
            self._attributes = {}
            for k, v in self._elem.attrib.items():
                ns, name = extract_namespace_name(k)
                self._attributes[(name, ns)] = v
        return self._attributes

    @property
    @drb.resolve_children
    def children(self) -> List[DrbNode]:
        if self._children is None:
            self._children = [XmlNode(e, self) for e in list(self._elem)]
        return self._children

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: int = None) -> Union[DrbNode,
                                                          List[DrbNode]]:
        try:
            found = [child for child in self.children
                     if child.name == name
                     and child.namespace_uri == namespace_uri]
            if occurrence is None and len(found) > 0:
                return [node for node in found]
            if occurrence > 0:
                return found[occurrence - 1]
            else:
                raise DrbException(f'Child ({name},{occurrence}) not found')
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child ({name},{occurrence}) not found') \
                from error

    def has_impl(self, impl: type) -> bool:
        return impl == str and not self.has_child()

    def get_impl(self, impl: type) -> Any:
        if self.has_impl(impl):
            return self.value
        raise DrbNotImplementationException(
            f"XmlNode doesn't implement {impl}")

    def close(self) -> None:
        pass


class XmlBaseNode(DrbLogicalNode):

    def __init__(self, node: DrbNode,
                 source: Union[BufferedIOBase, RawIOBase, IO]):
        """
        The given source is closed via this class #close() method.
        """
        DrbLogicalNode.__init__(self, source=node)
        self.base_node = node
        self.source = source
        xml_root = parse(source).getroot()
        self.xml_node = XmlNode(xml_root, parent=node)

    @property
    def children(self) -> List[DrbNode]:
        return [self.xml_node]

    def _get_named_child(self, name: str, namespace_uri: str = None,
                         occurrence: int = None) -> Union[DrbNode,
                                                          List[DrbNode]]:
        try:
            if self.xml_node.name == name and \
                    self.xml_node.namespace_uri == namespace_uri:
                if occurrence is None:
                    return [self.xml_node]
                elif occurrence == 1:
                    return self.xml_node
            raise DrbException(f'Child ({name},{occurrence}) not found')
        except (IndexError, TypeError) as error:
            raise DrbException(f'Child ({name},{occurrence}) not found') \
                from error

    def close(self) -> None:
        if self.source:
            self.source.close()
        # TBC: shall the base node be closes by base node creator (?)
        self.base_node.close()
