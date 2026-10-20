"""Bucket events into fixed rate windows.

Counters are accumulated per aligned window so a dashboard can render requests
per window without tracking individual timestamps.
"""
from collections import defaultdict


def window_start(timestamp, window_seconds):
    """Return the aligned start of the window holding the timestamp."""
    size = int(window_seconds)
    if size <= 0:
        raise ValueError("window_seconds must be positive")
    return (int(timestamp) // size) * size


def bucket_events(timestamps, window_seconds):
    """Group timestamps into ordered window buckets."""
    buckets = defaultdict(int)
    for stamp in timestamps:
        buckets[window_start(stamp, window_seconds)] += 1
    return dict(sorted(buckets.items()))


def peak_window(timestamps, window_seconds):
    """Return the busiest window start and its count."""
    buckets = bucket_events(timestamps, window_seconds)
    if not buckets:
        return None
    start = max(buckets, key=buckets.get)
    return start, buckets[start]


__all__ = ["window_start", "bucket_events", "peak_window"]
