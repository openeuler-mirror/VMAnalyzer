"""Downsample a time series into coarser buckets.

Aggregates timestamped samples into aligned buckets by mean or max so graphs
can render long ranges without keeping every raw point.
"""
from collections import defaultdict


def _bucket(timestamp, bucket_seconds):
    """Return the aligned bucket start for a timestamp."""
    size = int(bucket_seconds)
    if size <= 0:
        raise ValueError("bucket_seconds must be positive")
    return (int(timestamp) // size) * size


def downsample(samples, bucket_seconds, reducer="mean"):
    """Aggregate (timestamp, value) samples into aligned buckets."""
    grouped = defaultdict(list)
    for timestamp, value in samples:
        grouped[_bucket(timestamp, bucket_seconds)].append(float(value))
    result = {}
    for start in sorted(grouped):
        values = grouped[start]
        if reducer == "max":
            result[start] = max(values)
        elif reducer == "min":
            result[start] = min(values)
        else:
            result[start] = sum(values) / len(values)
    return result


__all__ = ["downsample"]
