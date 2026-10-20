"""Meeting-room allocation minimising the number of rooms needed.

This is the interval-partitioning problem: sorting the starts and the ends
independently and sweeping both pointers reveals how many rooms would be
required at the busiest moment, using two sorted arrays instead of events.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Meeting = Tuple[float, float]


def min_rooms(meetings: Iterable[Meeting]) -> int:
    """Return the smallest number of rooms that can host all meetings."""
    pairs = [(low, high) for low, high in meetings if high > low]
    if not pairs:
        return 0
    starts = sorted(low for low, _ in pairs)
    ends = sorted(high for _, high in pairs)
    rooms = 0
    best = 0
    end_pointer = 0
    for start in starts:
        while end_pointer < len(ends) and ends[end_pointer] <= start:
            rooms -= 1
            end_pointer += 1
        rooms += 1
        best = max(best, rooms)
    LOG.debug("rooms required %d", best)
    return best


def schedule_rooms(meetings: Iterable[Meeting]) -> List[List[Meeting]]:
    """Greedily assign meetings to rooms, reusing freed rooms first."""
    ordered = sorted(meetings)
    rooms: List[List[Meeting]] = []
    for meeting in ordered:
        placed = False
        for room in rooms:
            if room[-1][1] <= meeting[0]:
                room.append(meeting)
                placed = True
                break
        if not placed:
            rooms.append([meeting])
    return rooms


def utilizations(meetings: Iterable[Meeting]) -> float:
    """Return the ratio of meeting time to total spanned time."""
    ordered = sorted(meetings)
    if not ordered:
        return 0.0
    busy = sum(high - low for low, high in ordered)
    span = (max(high for _, high in ordered) - min(low for low, _ in ordered)) * len(meetings)
    return busy / span if span else 0.0


__all__ = ["min_rooms", "schedule_rooms", "utilizations"]
