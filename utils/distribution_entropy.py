"""Entropy and divergence measures for discrete distributions."""
import logging
import math

LOG = logging.getLogger(__name__)


def normalize(counts):
    """Return counts rescaled to a distribution summing to one."""
    items = [float(c) for c in counts or []]
    total = sum(items)
    if total <= 0:
        return []
    return [c / total for c in items]


def shannon_entropy(counts):
    """Return the Shannon entropy in nats of a count distribution."""
    probabilities = normalize(counts)
    return -sum(p * math.log(p) for p in probabilities if p > 0)


def relative_entropy(observed, expected):
    """Return the KL divergence from expected to observed distributions."""
    left = normalize(observed)
    right = normalize(expected)
    if len(left) != len(right) or not left:
        raise ValueError('distributions must be non-empty and equally sized')
    return sum(p * math.log(p / q)
               for p, q in zip(left, right) if p > 0 and q > 0)


__all__ = ['normalize', 'shannon_entropy', 'relative_entropy']
