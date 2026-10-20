"""Derive multiple bloom filter bit positions from one key."""
import hashlib
import logging
import math

LOG = logging.getLogger(__name__)


def double_hashes(key, size):
    """Return two independent hash values for a key."""
    if isinstance(key, str):
        key = key.encode('utf-8')
    first = int.from_bytes(hashlib.sha256(key + bytes([1])).digest()[:8], 'big')
    second = int.from_bytes(hashlib.sha256(key + bytes([2])).digest()[:8], 'big')
    return first % size, second % size


def bit_positions(key, size, count):
    """Return several bit positions using enhanced double hashing."""
    if count <= 0 or size <= 0:
        raise ValueError('size and count must be positive')
    first, second = double_hashes(key, size)
    step = second | 1
    return [(first + index * step) % size for index in range(count)]


def optimal_count(size, items):
    """Estimate the optimal number of hash functions for a bloom filter."""
    if not items or size <= 0:
        return 1
    return max(1, int(round((size / float(items)) * math.log(2))))


__all__ = ['double_hashes', 'bit_positions', 'optimal_count']
