"""Hypercall latency bucketing.

Hypercalls crossing into the host are cheap individually but expensive in
aggregate, so samples are folded into power of two latency buckets.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def bucket_of(latency_us):
    """Return the power of two bucket index for a latency in microseconds."""
    value = max(0.0, float(latency_us))
    if value <= 1.0:
        return 0
    return int(math.ceil(math.log(value, 2)))


def histogram(samples):
    """Return {bucket_index: count} for the given samples."""
    hist = {}
    for sample in samples or []:
        bucket = bucket_of(sample)
        hist[bucket] = hist.get(bucket, 0) + 1
    return dict(sorted(hist.items()))


def tail_share(samples, threshold_us=64.0):
    """Return the share of samples slower than the threshold."""
    clean = [float(s) for s in samples or [] if s is not None]
    if not clean:
        return 0.0
    slow = sum(1 for s in clean if s > threshold_us)
    LOG.debug('hypercall tail %d/%d', slow, len(clean))
    return round(slow / float(len(clean)), 3)


__all__ = ['bucket_of', 'histogram', 'tail_share']
