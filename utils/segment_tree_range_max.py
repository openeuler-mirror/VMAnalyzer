"""Iterative segment tree answering range-maximum queries.

The tree is stored in a flat array of size ``2 * n`` where ``n`` is the next
power of two above the input length.  Leaves hold the original values and
internal nodes hold the maximum of their children, so updates walk upward
while queries combine O(log n) canonical nodes.
"""

import logging
from typing import List, Sequence

LOG = logging.getLogger(__name__)


class RangeMaxTree:
    """Segment tree supporting point updates and range maxima."""

    def __init__(self, values: Sequence[float]) -> None:
        size = 1
        while size < max(1, len(values)):
            size <<= 1
        self._size = size
        self._tree = [float("-inf")] * (2 * size)
        for index, value in enumerate(values):
            self._tree[size + index] = value
        for index in range(size - 1, 0, -1):
            self._tree[index] = max(self._tree[2 * index], self._tree[2 * index + 1])

    def update(self, index: int, value: float) -> None:
        """Set the leaf at *index* to *value* and refresh its ancestors."""
        node = self._size + index
        self._tree[node] = value
        node //= 2
        while node:
            self._tree[node] = max(self._tree[2 * node], self._tree[2 * node + 1])
            node //= 2

    def query(self, left: int, right: int) -> float:
        """Maximum value on the half-open range ``[left, right)``."""
        lo = left + self._size
        hi = right + self._size
        best = float("-inf")
        while lo < hi:
            if lo & 1:
                best = max(best, self._tree[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                best = max(best, self._tree[hi])
            lo //= 2
            hi //= 2
        return best


def build(values: Sequence[float]) -> RangeMaxTree:
    """Build a range maximum tree from a sequence of numbers."""
    LOG.debug("building range max tree of %d values", len(values))
    return RangeMaxTree(values)


__all__ = ["RangeMaxTree", "build"]
