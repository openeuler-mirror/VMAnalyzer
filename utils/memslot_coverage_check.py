"""Check that guest memory regions are covered by host memslots.

Uncovered regions force QEMU to fall back to slower paths or fail at
startup with an opaque error.  Comparing covered ranges with the declared
guest RAM exposes gaps early.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Range = Tuple[int, int]


def merge(ranges: Iterable[Range]) -> List[Range]:
    """Merge overlapping address ranges."""
    ordered = sorted((min(low, high), max(low, high)) for low, high in ranges)
    merged: List[Range] = []
    for low, high in ordered:
        if merged and low <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], high))
            continue
        merged.append((low, high))
    return merged


def gaps(covered: Iterable[Range], required: Range) -> List[Range]:
    """Return the parts of *required* not covered by the supplied ranges."""
    low, high = required
    holes: List[Range] = []
    cursor = low
    for start, end in merge(covered):
        if end < cursor or start > high:
            continue
        if start > cursor:
            holes.append((cursor, min(start, high)))
        cursor = max(cursor, end)
        if cursor >= high:
            break
    if cursor < high:
        holes.append((cursor, high))
    if holes:
        LOG.warning("%d memslot coverage gap(s) detected", len(holes))
    return holes


def fully_covered(covered: Iterable[Range], required: Range) -> bool:
    """Return True when the required range has no uncovered bytes."""
    return not gaps(covered, required)


__all__ = ["Range", "merge", "gaps", "fully_covered"]
