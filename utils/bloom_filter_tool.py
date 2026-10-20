"""Bloom filter sizing helper.

Bloom filters trade memory for a tunable false positive rate; the bit count
and hash count are derived from the expected item count.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def optimal_bits(expected_items, fp_rate):
    """Return the bit array size for the target false positive rate."""
    n = max(1, int(expected_items or 1))
    p = min(0.5, max(1e-9, float(fp_rate or 0.01)))
    bits = -n * math.log(p) / (math.log(2) ** 2)
    LOG.debug('bloom bits %.0f for n=%d p=%.4f', bits, n, p)
    return int(math.ceil(bits))


def optimal_hashes(bits, expected_items):
    """Return the hash function count for the sized filter."""
    n = max(1, int(expected_items or 1))
    return max(1, int(round(bits / float(n) * math.log(2))))


__all__ = ['optimal_bits', 'optimal_hashes']
