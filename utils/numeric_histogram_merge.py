"""Merge two histograms that share identical bin boundaries.

Collected metric snapshots are often aggregated per host.  Merging raw
counts is cheaper and more accurate than recomputing percentiles from the
original samples, provided the bin edges match exactly.
"""

import logging
from typing import Dict, List, Sequence, Tuple

LOG = logging.getLogger(__name__)


def merge_histograms(left: Sequence[Tuple[float, int]],
                     right: Sequence[Tuple[float, int]]) -> List[Tuple[float, int]]:
    """Sum counts for matching bin edges and keep the union of edges."""
    totals: Dict[float, int] = {}
    for edge, count in list(left) + list(right):
        totals[edge] = totals.get(edge, 0) + int(count)
    merged = sorted(totals.items(), key=lambda item: item[0])
    LOG.debug("merged %d and %d bins into %d bins", len(left), len(right), len(merged))
    return merged


def total_count(histogram: Sequence[Tuple[float, int]]) -> int:
    """Return the number of observations represented by *histogram*."""
    return sum(int(count) for _, count in histogram)


def edges_match(left: Sequence[Tuple[float, int]],
                right: Sequence[Tuple[float, int]]) -> bool:
    """Check whether both histograms use the same ordered bin edges."""
    left_edges = [edge for edge, _ in left]
    right_edges = [edge for edge, _ in right]
    matches = len(left_edges) == len(right_edges) and all(
        abs(a - b) < 1e-9 for a, b in zip(left_edges, right_edges)
    )
    if not matches:
        LOG.warning("histogram edges differ, counts are not directly comparable")
    return matches


__all__ = ["merge_histograms", "total_count", "edges_match"]
