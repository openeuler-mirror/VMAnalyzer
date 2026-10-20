"""K-minimum-values distinct counter.

Keeping the k smallest hashes estimates cardinality as k over the k-th hash;
the estimate is unbiased for streams.
"""
import logging

LOG = logging.getLogger(__name__)


def cardinality(k_smallest, k, hash_max=1.0):
    """Return the distinct-count estimate from the k-th smallest hash."""
    vals = sorted(float(v) for v in k_smallest or [] if v is not None)
    if len(vals) < int(k or 1) or not vals:
        return float(len(vals))
    kth = vals[int(k) - 1]
    if kth <= 0:
        return 0.0
    est = (int(k) - 1) * float(hash_max or 1.0) / kth
    LOG.debug('kmv estimate %.0f', est)
    return round(est, 1)


def memory_words(k):
    """Return the storage words needed to keep k minima."""
    return max(1, int(k or 1))


__all__ = ['cardinality', 'memory_words']
