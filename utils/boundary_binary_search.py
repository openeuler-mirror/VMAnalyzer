"""Boundary binary search over monotone predicates and sorted sequences.

Unlike a plain membership search, these helpers locate the transition point
between False and True regions.  They are the building blocks for
"first index that satisfies" style queries used across scheduling code.
"""

import logging
from typing import Callable, List, Optional, Sequence

LOG = logging.getLogger(__name__)


def lower_bound(data: Sequence, target) -> int:
    """First index whose value is not less than *target*."""
    low, high = 0, len(data)
    while low < high:
        mid = (low + high) // 2
        if data[mid] < target:
            low = mid + 1
        else:
            high = mid
    return low


def upper_bound(data: Sequence, target) -> int:
    """First index whose value is strictly greater than *target*."""
    low, high = 0, len(data)
    while low < high:
        mid = (low + high) // 2
        if data[mid] <= target:
            low = mid + 1
        else:
            high = mid
    return low


def first_true(size: int, predicate: Callable[[int], bool]) -> Optional[int]:
    """Smallest index in ``[0, size)`` where *predicate* first turns True."""
    low, high = 0, size
    while low < high:
        mid = (low + high) // 2
        if predicate(mid):
            high = mid
        else:
            low = mid + 1
    if low < size:
        LOG.debug("transition found at index %d", low)
        return low
    return None


def count_equal(data: Sequence, target) -> int:
    """Number of elements equal to *target* in a sorted sequence."""
    return upper_bound(data, target) - lower_bound(data, target)


__all__ = ["lower_bound", "upper_bound", "first_true", "count_equal"]
