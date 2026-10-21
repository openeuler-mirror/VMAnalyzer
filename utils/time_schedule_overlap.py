"""Detect overlapping maintenance windows across hosts.

Rolling maintenance plans frequently collide because each host declares
its own window independently.  Grouping overlapping intervals early avoids
simultaneous evacuations of the same storage backend.
"""

import logging
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Window = Tuple[float, float]


def find_overlaps(windows: Dict[str, Window]) -> List[Tuple[str, str, float]]:
    """Return ``(host_a, host_b, overlap_seconds)`` for every collision."""
    items = sorted(windows.items(), key=lambda item: item[1][0])
    overlaps: List[Tuple[str, str, float]] = []
    for index, (name, (start, end)) in enumerate(items):
        for other, (other_start, other_end) in items[index + 1:]:
            if other_start >= end:
                break
            shared = min(end, other_end) - max(start, other_start)
            if shared > 0:
                overlaps.append((name, other, float(shared)))
    if overlaps:
        LOG.warning("found %d overlapping maintenance window(s)", len(overlaps))
    return overlaps


def merge_windows(windows: Iterable[Window]) -> List[Window]:
    """Merge touching or overlapping intervals into a minimal covering set."""
    merged: List[Window] = []
    for start, end in sorted(windows):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            continue
        merged.append((start, end))
    LOG.debug("merged into %d disjoint window(s)", len(merged))
    return merged


__all__ = ["Window", "find_overlaps", "merge_windows"]
