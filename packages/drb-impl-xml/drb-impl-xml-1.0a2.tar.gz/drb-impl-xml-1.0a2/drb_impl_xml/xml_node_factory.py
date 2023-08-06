from io import BufferedIOBase

from drb import DrbNode
from .xml_node import XmlBaseNode
from drb.factory.factory import DrbFactory


class XmlNodeFactory(DrbFactory):

    def _create(self, node: DrbNode) -> DrbNode:
        return XmlBaseNode(node, node.get_impl(BufferedIOBase))
