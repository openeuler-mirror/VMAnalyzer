"""Compute the percentile rank of each value within a series.

Percentile rank answers "what share of samples is at or below this value",
which is the right question when comparing one VM against its peers
without assuming a normal distribution.
"""

import logging
from typing import Dict, List, Sequence

LOG = logging.getLogger(__name__)


def percentile_ranks(values: Sequence[float]) -> List[float]:
    """Return the 0-100 percentile rank for every input position."""
    if not values:
        return []
    ordered = sorted(float(value) for value in values)
    total = len(ordered)
    cache: Dict[float, float] = {}
    for value in set(ordered):
        below = 0
        equal = 0
        for candidate in ordered:
            if candidate < value:
                below += 1
            elif candidate == value:
                equal += 1
        cache[value] = (below + 0.5 * equal) / total * 100.0
    ranks = [round(cache[float(value)], 4) for value in values]
    LOG.debug("computed percentile ranks for %d values", total)
    return ranks


def rank_of(value: float, reference: Sequence[float]) -> float:
    """Return the percentile rank of a single value against *reference*."""
    if not reference:
        return 0.0
    below = sum(1 for item in reference if item < value)
    equal = sum(1 for item in reference if item == value)
    return round((below + 0.5 * equal) / len(reference) * 100.0, 4)


__all__ = ["percentile_ranks", "rank_of"]
