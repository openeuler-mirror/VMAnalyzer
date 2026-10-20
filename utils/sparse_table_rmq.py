"""Sparse table giving O(1) range minimum queries after preprocessing.

The table has one level per power of two.  Level ``k`` stores the minimum of
windows of width ``2 ** k``, so any query range is answered by overlapping two
windows whose width equals the largest power of two fitting the range.
"""

import logging
from typing import List, Sequence

LOG = logging.getLogger(__name__)


class SparseTableMin:
    """Precompute overlapping blocks to answer range minimums in O(1)."""

    def __init__(self, values: Sequence[int]) -> None:
        base = list(values)
        size = len(base)
        levels = max(1, size.bit_length())
        self._table: List[List[int]] = [base]
        for level in range(1, levels):
            previous = self._table[level - 1]
            span = 1 << (level - 1)
            width = 1 << level
            self._table.append(
                [min(previous[i], previous[i + span]) for i in range(size - width + 1)]
            )
        LOG.debug("sparse table built with %d levels", len(self._table))

    def minimum(self, left: int, right: int) -> int:
        """Minimum value on the inclusive range ``[left, right]``."""
        length = right - left + 1
        level = length.bit_length() - 1
        span = 1 << level
        row = self._table[level]
        return min(row[left], row[right - span + 1])


def query_min(values: Sequence[int], left: int, right: int) -> int:
    """One-shot range minimum for callers without a reusable table."""
    return SparseTableMin(values).minimum(left, right)


__all__ = ["SparseTableMin", "query_min"]
