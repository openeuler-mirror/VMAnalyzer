"""RCU stall event tracking.

RCU stalls precede full hangs; counting stalls per grace period bucket shows
whether the system is degrading over time.
"""
import logging

LOG = logging.getLogger(__name__)


def stalls_per_bucket(timestamps, bucket_sec=300.0):
    """Return {bucket_index: stall_count} for the given timestamps."""
    buckets = {}
    for stamp in timestamps or []:
        bucket = int(float(stamp) // float(bucket_sec))
        buckets[bucket] = buckets.get(bucket, 0) + 1
    return dict(sorted(buckets.items()))


def is_escalating(timestamps, bucket_sec=300.0):
    """Report when the last bucket has more stalls than the first."""
    buckets = stalls_per_bucket(timestamps, bucket_sec)
    if len(buckets) < 2:
        return False
    values = list(buckets.values())
    LOG.debug('stall buckets %s', values)
    return values[-1] > values[0]


__all__ = ['stalls_per_bucket', 'is_escalating']
