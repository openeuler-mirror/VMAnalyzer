"""Cuckoo filter capacity planner.

Cuckoo filters support deletion but degrade past 95 percent occupancy, so
fingerprint capacity is computed with headroom.
"""
import logging

LOG = logging.getLogger(__name__)


def bucket_count(expected_items, bucket_size=4, max_load=0.95):
    """Return the bucket count for the expected item count."""
    n = max(1, int(expected_items or 1))
    buckets = int(n / (bucket_size * max_load)) + 1
    LOG.debug('cuckoo buckets %d for %d items', buckets, n)
    return buckets


def fingerprint_bits(expected_items, fp_rate):
    """Return fingerprint bits for the target false positive rate."""
    import math
    n = max(1, int(expected_items or 1))
    p = min(0.5, max(1e-9, float(fp_rate or 0.01)))
    return max(1, int(math.ceil(math.log(2.0 / p, 2))))


__all__ = ['bucket_count', 'fingerprint_bits']
