"""Clamp slicing bounds against a sequence length before indexing.

Metric buffers are indexed with values derived from counters, and an
off-by-one during startup can raise IndexError.  Clamping first keeps the
collection loop exception free without hiding genuine logic errors.
"""

import logging
from typing import Sequence, Tuple

LOG = logging.getLogger(__name__)


def clamp_window(start: int, stop: int, length: int) -> Tuple[int, int]:
    """Return bounds clamped into ``[0, length]`` with ``start <= stop``."""
    if length < 0:
        raise ValueError("length must not be negative")
    low = max(0, min(int(start), length))
    high = max(0, min(int(stop), length))
    if high < low:
        LOG.debug("swapped reversed window %d..%d", low, high)
        low, high = high, low
    return low, high


def safe_slice(items: Sequence, start: int, stop: int) -> Sequence:
    """Slice *items* using clamped bounds."""
    low, high = clamp_window(start, stop, len(items))
    return items[low:high]


def tail(items: Sequence, count: int) -> Sequence:
    """Return at most the last *count* items."""
    if count <= 0:
        return items[0:0]
    low, high = clamp_window(len(items) - count, len(items), len(items))
    return items[low:high]


__all__ = ["clamp_window", "safe_slice", "tail"]
