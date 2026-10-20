"""Sweep-line counter for maximum interval overlap depth.

Each interval contributes a start event and an end event.  Sorting events by
coordinate and applying start-before-end tie breaking yields the point of
greatest concurrency, which is the classic resource pressure question.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Interval = Tuple[float, float]
Event = Tuple[float, int]


def max_overlap(intervals: Iterable[Interval]) -> int:
    """Return the highest number of simultaneously open intervals."""
    events: List[Event] = []
    for low, high in intervals:
        if high > low:
            events.append((low, 1))
            events.append((high, -1))
    events.sort(key=lambda event: (event[0], -event[1]))
    current = best = 0
    for _, delta in events:
        current += delta
        best = max(best, current)
    LOG.debug("peak overlap depth %d", best)
    return best


def overlap_profile(intervals: Iterable[Interval]) -> List[Tuple[float, int]]:
    """Return running depth after each distinct event coordinate."""
    events: List[Event] = []
    for low, high in intervals:
        events.append((low, 1))
        events.append((high, -1))
    events.sort(key=lambda event: (event[0], -event[1]))
    profile: List[Tuple[float, int]] = []
    current = 0
    for coordinate, delta in events:
        current += delta
        profile.append((coordinate, current))
    return profile


def busiest_point(intervals: Iterable[Interval]) -> Tuple[float, int]:
    """Return the coordinate with the greatest overlap and that depth."""
    profile = overlap_profile(intervals)
    if not profile:
        return 0.0, 0
    return max(profile, key=lambda item: item[1])


__all__ = ["max_overlap", "overlap_profile", "busiest_point"]
