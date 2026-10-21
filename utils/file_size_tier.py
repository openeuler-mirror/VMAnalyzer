"""Bucket byte sizes into operational storage tiers.

Capacity dashboards work better with tiers such as "small", "large" and
"huge" than with raw byte counts.  Tiers also make anomaly thresholds
portable across storage backends with different hardware.
"""

import logging
from typing import Dict, Iterable

LOG = logging.getLogger(__name__)

TIER_BOUNDS = (
    ("tiny", 1024 ** 2),
    ("small", 1024 ** 3),
    ("medium", 10 * 1024 ** 3),
    ("large", 100 * 1024 ** 3),
)


def size_tier(size_bytes: float) -> str:
    """Return the tier label for a byte count."""
    for label, limit in TIER_BOUNDS:
        if size_bytes < limit:
            return label
    return "huge"


def tier_counts(sizes: Iterable[float]) -> Dict[str, int]:
    """Count how many file sizes fall into each tier."""
    counts: Dict[str, int] = {}
    for size in sizes:
        label = size_tier(float(size))
        counts[label] = counts.get(label, 0) + 1
    LOG.debug("size tier counts %s", counts)
    return counts


def largest_tier_share(sizes: Iterable[float]) -> float:
    """Return the share of total bytes held by the largest single tier."""
    totals: Dict[str, float] = {}
    for size in sizes:
        label = size_tier(float(size))
        totals[label] = totals.get(label, 0.0) + float(size)
    overall = sum(totals.values())
    if overall <= 0:
        return 0.0
    return round(max(totals.values()) / overall, 4)


__all__ = ["TIER_BOUNDS", "size_tier", "tier_counts", "largest_tier_share"]
