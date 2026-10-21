"""Quantify how bursty a log stream is compared with its own average.

Bursts of identical errors indicate retry storms rather than independent
failures.  The burst index compares the busiest interval with the mean,
which is simple to explain during an incident review.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)


def bucket_counts(timestamps: Iterable[float], interval: float = 60.0) -> List[int]:
    """Count events per aligned interval, including empty intervals."""
    values = sorted(float(timestamp) for timestamp in timestamps)
    if not values:
        return []
    if interval <= 0:
        raise ValueError("interval must be positive")
    start = values[0] - (values[0] % interval)
    end = values[-1]
    count = int((end - start) // interval) + 1
    buckets = [0] * count
    for value in values:
        buckets[int((value - start) // interval)] += 1
    return buckets


def burst_index(timestamps: Iterable[float], interval: float = 60.0) -> float:
    """Return peak bucket count divided by the mean bucket count."""
    buckets = bucket_counts(timestamps, interval)
    if not buckets:
        return 0.0
    mean = sum(buckets) / len(buckets)
    if mean == 0:
        return 0.0
    index = max(buckets) / mean
    LOG.debug("burst index %.2f across %d interval(s)", index, len(buckets))
    return round(index, 2)


def busiest_window(timestamps: Iterable[float], interval: float = 60.0) -> Tuple[int, int]:
    """Return the busiest bucket index and its count."""
    buckets = bucket_counts(timestamps, interval)
    if not buckets:
        return 0, 0
    index = max(range(len(buckets)), key=lambda position: buckets[position])
    return index, buckets[index]


__all__ = ["bucket_counts", "burst_index", "busiest_window"]
