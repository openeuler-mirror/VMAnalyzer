"""Calendar slot allocator finding free windows for a booking.

Busy blocks are clipped to the working day and merged, then the gaps between
them become candidate windows.  Allocation simply returns the earliest gap
large enough for the requested duration.
"""

import logging
from typing import Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)

Span = Tuple[float, float]


def free_windows(busy: Iterable[Span], day_start: float, day_end: float) -> List[Span]:
    """Return the gaps between merged busy blocks inside the working day."""
    merged: List[Span] = []
    for start, end in sorted(busy):
        start = max(start, day_start)
        end = min(end, day_end)
        if start >= end:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    windows: List[Span] = []
    cursor = day_start
    for start, end in merged:
        if start > cursor:
            windows.append((cursor, start))
        cursor = max(cursor, end)
    if cursor < day_end:
        windows.append((cursor, day_end))
    LOG.debug("found %d free windows", len(windows))
    return windows


def allocate_slot(busy: Iterable[Span], day_start: float, day_end: float,
                  duration: float) -> Optional[Span]:
    """Return the earliest free slot of *duration* inside the day."""
    for start, end in free_windows(busy, day_start, day_end):
        if end - start >= duration:
            return start, start + duration
    LOG.info("no free slot of %.1f available", duration)
    return None


def free_minutes(busy: Iterable[Span], day_start: float, day_end: float) -> float:
    """Return the total free time inside the working day."""
    return sum(end - start for start, end in free_windows(busy, day_start, day_end))


__all__ = ["free_windows", "allocate_slot", "free_minutes"]
