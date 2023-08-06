from typing import Any, List

from drb import DrbNode
from drb.factory import DrbFactory
from drb.utils.logical_node import DrbLogicalNode

from drb_impl_image.image_node import DrbImageNode


class DrbImageBaseNode(DrbLogicalNode):

    def __init__(self, base_node: DrbNode):
        DrbLogicalNode.__init__(self, source=base_node)
        self.base_node = base_node
        self._children = [DrbImageNode(self)]

    @property
    def children(self) -> List[DrbNode]:
        return self._children

    def close(self):
        if self._children is not None:
            self._children[0].close()
        self.base_node.close()

    def has_impl(self, impl: type) -> bool:
        return self._wrapped_node.has_impl(impl)

    def get_impl(self, impl: type) -> Any:
        return self._wrapped_node.get_impl(impl)


class DrbImageFactory(DrbFactory):

    def _create(self, node: DrbNode) -> DrbNode:
        return DrbImageBaseNode(base_node=node)
