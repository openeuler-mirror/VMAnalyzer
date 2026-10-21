"""Merge numeric ranges and report their total coverage.

Disk block lists and NUMA address ranges arrive as overlapping numeric
pairs.  Merging them gives both the real footprint and a canonical form
for equality checks between hosts.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Range = Tuple[float, float]


def merge_ranges(ranges: Iterable[Range], tolerance: float = 0.0) -> List[Range]:
    """Merge overlapping or adjacent ranges into disjoint intervals."""
    ordered = sorted((min(start, end), max(start, end)) for start, end in ranges)
    merged: List[Range] = []
    for start, end in ordered:
        if merged and start <= merged[-1][1] + tolerance:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            continue
        merged.append((start, end))
    LOG.debug("merged into %d disjoint range(s)", len(merged))
    return merged


def total_coverage(ranges: Iterable[Range]) -> float:
    """Return the total length covered by the merged ranges."""
    return sum(end - start for start, end in merge_ranges(ranges))


def covers_point(ranges: Iterable[Range], point: float) -> bool:
    """Return True when *point* lies inside any supplied range."""
    return any(start <= point <= end for start, end in merge_ranges(ranges))


__all__ = ["Range", "merge_ranges", "total_coverage", "covers_point"]
