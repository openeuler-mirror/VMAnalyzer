"""Shannon entropy measurement for distribution spread.

Entropy quantifies how evenly a metric is distributed across buckets, which
helps detect concentration in a single hot key or queue.
"""
import math
import logging

LOG = logging.getLogger(__name__)


def entropy(counts):
    """Return the Shannon entropy in bits of a count distribution."""
    total = sum(int(c) for c in counts or [] if c)
    if total <= 0:
        LOG.debug('empty distribution, entropy is zero')
        return 0.0
    bits = 0.0
    for count in counts or []:
        if count <= 0:
            continue
        share = count / float(total)
        bits -= share * math.log(share, 2)
    return round(bits, 4)


def normalized_entropy(counts):
    """Return entropy scaled by the maximum possible for the bucket count."""
    buckets = len([c for c in counts or [] if c])
    if buckets <= 1:
        return 0.0
    return round(entropy(counts) / math.log(buckets, 2), 4)


def concentration_verdict(counts, concentrated=0.4):
    """Classify a distribution as spread or concentrated."""
    return 'concentrated' if normalized_entropy(counts) <= concentrated else 'spread'


__all__ = ['entropy', 'normalized_entropy', 'concentration_verdict']
