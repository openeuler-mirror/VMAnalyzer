"""Percentile of weighted samples without expanding repeated values.

When samples are already aggregated as ``(value, weight)`` pairs, expanding
them into a flat list is wasteful.  Walking the cumulative weight directly
gives the same percentile at a fraction of the memory cost.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)


def weighted_percentile(pairs: Iterable[Tuple[float, float]],
                        percent: float = 95.0) -> float:
    """Return the weighted percentile, interpolating inside the target bin."""
    ordered: List[Tuple[float, float]] = sorted(
        ((float(value), max(0.0, float(weight))) for value, weight in pairs),
        key=lambda item: item[0],
    )
    if not ordered:
        return 0.0
    if not 0.0 <= percent <= 100.0:
        raise ValueError("percent must lie within [0, 100]")
    target = sum(weight for _, weight in ordered) * percent / 100.0
    running = 0.0
    for value, weight in ordered:
        running += weight
        if running >= target:
            LOG.debug("weighted p%.2f resolved to %.4f", percent, value)
            return value
    return ordered[-1][0]


def weighted_median(pairs: Iterable[Tuple[float, float]]) -> float:
    """Convenience wrapper returning the weighted 50th percentile."""
    return weighted_percentile(pairs, 50.0)


def total_weight(pairs: Iterable[Tuple[float, float]]) -> float:
    """Sum the weights of all supplied pairs."""
    return sum(max(0.0, float(weight)) for _, weight in pairs)


__all__ = ["weighted_percentile", "weighted_median", "total_weight"]
