"""Merge overlapping or touching closed intervals into a minimal cover.

Intervals are sorted by their lower endpoint and then folded left to right.
Each new interval either extends the current run or starts a fresh run when a
gap separates it from the accumulation.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Interval = Tuple[float, float]


def merge_intervals(intervals: Iterable[Interval], touch_epsilon: float = 0.0) -> List[Interval]:
    """Collapse intervals that overlap or lie within *touch_epsilon*."""
    ordered = sorted(intervals)
    if not ordered:
        return []
    merged: List[Interval] = [ordered[0]]
    for low, high in ordered[1:]:
        current_low, current_high = merged[-1]
        if low <= current_high + touch_epsilon:
            merged[-1] = (current_low, max(current_high, high))
        else:
            merged.append((low, high))
    LOG.debug("merged %d intervals into %d runs", len(ordered), len(merged))
    return merged


def total_coverage(intervals: Iterable[Interval]) -> float:
    """Return the summed length of a merged interval set."""
    return sum(high - low for low, high in merge_intervals(intervals))


def complement_gaps(intervals: Iterable[Interval], start: float, end: float) -> List[Interval]:
    """Return the uncovered spans of ``[start, end]`` after merging."""
    gaps: List[Interval] = []
    cursor = start
    for low, high in merge_intervals(intervals):
        if low > cursor:
            gaps.append((cursor, low))
        cursor = max(cursor, high)
    if cursor < end:
        gaps.append((cursor, end))
    return gaps


__all__ = ["merge_intervals", "total_coverage", "complement_gaps"]
