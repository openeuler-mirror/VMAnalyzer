"""Ordered container with logarithmic insertion and rank queries.

Values are kept sorted in a flat list so that membership tests, rank
computation and bounded counting all reduce to bisection over contiguous
memory.  It trades O(n) insertion cost for cache friendly scans.
"""

import bisect
import logging
from typing import Iterable, List, Optional, Sequence

LOG = logging.getLogger(__name__)


class SortedContainer:
    """Keep values ordered to support rank and range counting."""

    def __init__(self, values: Optional[Iterable[float]] = None) -> None:
        self._data: List[float] = sorted(values) if values is not None else []

    def add(self, value: float) -> int:
        """Insert *value* keeping order and return the inserted index."""
        position = bisect.bisect_left(self._data, value)
        self._data.insert(position, value)
        return position

    def rank(self, value: float) -> int:
        """Number of stored items strictly less than *value*."""
        return bisect.bisect_left(self._data, value)

    def count_between(self, low: float, high: float) -> int:
        """Count items inside the inclusive range ``[low, high]``."""
        return bisect.bisect_right(self._data, high) - bisect.bisect_left(self._data, low)

    def snapshot(self) -> List[float]:
        """Return a defensive copy of the ordered values."""
        return list(self._data)

    def __len__(self) -> int:
        return len(self._data)


def merge_containers(containers: Sequence[SortedContainer]) -> SortedContainer:
    """Merge several sorted containers into a single ordered container."""
    combined: List[float] = []
    for container in containers:
        combined.extend(container.snapshot())
    return SortedContainer(combined)


__all__ = ["SortedContainer", "merge_containers"]
