"""Union-find set using union by rank with path compression.

Each disjoint set is a tree whose representative is the root.  Smaller rank
trees attach under larger ones and lookups flatten their paths, giving an
effectively constant amortised cost per operation.
"""

import logging
from typing import List

LOG = logging.getLogger(__name__)


class UnionFindRank:
    """Disjoint sets merging lower rank trees into higher rank trees."""

    def __init__(self, size: int) -> None:
        self._parent: List[int] = list(range(size))
        self._rank: List[int] = [0] * size
        self._count = size

    def find(self, item: int) -> int:
        """Return the representative of *item*, compressing the path."""
        root = item
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[item] != root:
            self._parent[item], item = root, self._parent[item]
        return root

    def union(self, left: int, right: int) -> bool:
        """Merge the sets of *left* and *right*; True when they differed."""
        root_left = self.find(left)
        root_right = self.find(right)
        if root_left == root_right:
            return False
        if self._rank[root_left] < self._rank[root_right]:
            root_left, root_right = root_right, root_left
        self._parent[root_right] = root_left
        if self._rank[root_left] == self._rank[root_right]:
            self._rank[root_left] += 1
        self._count -= 1
        LOG.debug("merged sets, %d remaining", self._count)
        return True

    def component_count(self) -> int:
        """Number of disjoint sets currently tracked."""
        return self._count


__all__ = ["UnionFindRank"]
