"""Hamming distance and similarity for integers and bit patterns."""
import logging

LOG = logging.getLogger(__name__)


def hamming_distance(left, right):
    """Return the number of differing bits between two non-negative integers."""
    a, b = int(left), int(right)
    if a < 0 or b < 0:
        raise ValueError('inputs must be non-negative')
    return bin(a ^ b).count('1')


def hamming_similarity(left, right, width):
    """Return the fraction of identical bits over the given bit width."""
    if width <= 0:
        return 0.0
    return 1.0 - hamming_distance(left, right) / float(width)


def hamming_many(reference, candidates):
    """Return the Hamming distance from reference to each candidate."""
    return [hamming_distance(reference, item) for item in candidates or []]


__all__ = ['hamming_distance', 'hamming_similarity', 'hamming_many']
