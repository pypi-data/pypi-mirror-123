from typing import Any, List, Dict, Optional, Tuple

import drb

from drb import DrbNode
from drb.exceptions import DrbNotImplementationException
from drb.utils.logical_node import DrbLogicalNode


class DrbImageListNode(DrbLogicalNode):

    def __init__(self, parent: DrbNode, name: str):
        path = parent.path / name
        DrbLogicalNode.__init__(self, path, parent=parent)
        self._children: List[DrbNode] = []

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return {}

    @property
    @drb.resolve_children
    def children(self) -> List[DrbNode]:
        return self._children

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type) -> Any:
        raise DrbNotImplementationException(f'no {impl} implementation found')
