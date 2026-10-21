"""Rank values with ties receiving the average of their positions.

Average ranking keeps correlation and weighting routines stable when many
samples share the same value, which is common for integer counters that
saturate or for metrics reported with coarse granularity.
"""

import logging
from typing import Dict, List, Sequence

LOG = logging.getLogger(__name__)


def average_ranks(values: Sequence[float]) -> List[float]:
    """Return 1-based average ranks aligned with the input order."""
    order = sorted(range(len(values)), key=lambda index: values[index])
    ranks = [0.0] * len(values)
    position = 0
    while position < len(order):
        end = position
        while end + 1 < len(order) and values[order[end + 1]] == values[order[position]]:
            end += 1
        share = (position + end) / 2.0 + 1.0
        for offset in range(position, end + 1):
            ranks[order[offset]] = share
        position = end + 1
    LOG.debug("ranked %d values with %d distinct levels", len(values), len(set(values)))
    return ranks


def rank_map(values: Sequence[float]) -> Dict[float, float]:
    """Map each distinct value to its average rank."""
    ranks = average_ranks(values)
    mapping: Dict[float, float] = {}
    for value, rank in zip(values, ranks):
        mapping[value] = rank
    return mapping


def top_indices(values: Sequence[float], limit: int = 3) -> List[int]:
    """Return indices of the highest values, preserving input order on ties."""
    ranked = average_ranks(values)
    limit = max(0, min(int(limit), len(values)))
    return sorted(sorted(range(len(values)), key=lambda i: -ranked[i])[:limit])


__all__ = ["average_ranks", "rank_map", "top_indices"]
