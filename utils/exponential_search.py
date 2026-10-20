"""Exponential search for sorted sequences and unbounded probes.

The probe bound doubles until it brackets the target, after which a normal
binary search finishes the job.  This is efficient when the target sits near
the front or when the sequence length is not known ahead of time.
"""

import logging
from typing import List, Optional, Sequence

LOG = logging.getLogger(__name__)


def exponential_search(data: Sequence, target) -> int:
    """Return the index of *target* in a sorted sequence or -1."""
    if not data:
        return -1
    if data[0] == target:
        return 0
    bound = 1
    while bound < len(data) and data[bound] <= target:
        bound *= 2
    low, high = bound // 2, min(bound, len(data) - 1)
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            LOG.debug("found target at %d", mid)
            return mid
        if data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def first_greater(data: Sequence, target) -> Optional[int]:
    """Index of the first element strictly greater than *target*."""
    bound = 1
    while bound < len(data) and data[bound] <= target:
        bound *= 2
    low, high = bound // 2, min(bound, len(data) - 1)
    while low <= high:
        mid = (low + high) // 2
        if data[mid] > target:
            if mid == 0 or data[mid - 1] <= target:
                return mid
            high = mid - 1
        else:
            low = mid + 1
    return None


def probe_bounds(data: Sequence, target) -> List[int]:
    """Return the bracketing window found by doubling probes."""
    bound = 1
    while bound < len(data) and data[bound] <= target:
        bound *= 2
    return [bound // 2, min(bound, len(data) - 1)]


__all__ = ["exponential_search", "first_greater", "probe_bounds"]
