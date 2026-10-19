"""MurmurHash3 x86 32-bit.

Murmur3 spreads similar keys evenly, which keeps hash tables and
partitioners balanced on real-world key sets.
"""
import logging

LOG = logging.getLogger(__name__)
MASK = 0xFFFFFFFF


def _rotl(value, count):
    return ((value << count) | (value >> (32 - count))) & MASK


def _fmix(h):
    h ^= h >> 16
    h = (h * 0x85EBCA6B) & MASK
    h ^= h >> 13
    h = (h * 0xC2B2AE35) & MASK
    h ^= h >> 16
    return h


def murmur3_32(data, seed=0):
    """Return the MurmurHash3 32-bit digest of bytes-like data."""
    buf = bytes(data)
    h = seed & MASK
    for i in range(0, len(buf) - len(buf) % 4, 4):
        k = int.from_bytes(buf[i:i + 4], 'little')
        k = (k * 0xCC9E2D51) & MASK
        k = (_rotl(k, 15) * 0x1B873593) & MASK
        h = _rotl(h ^ k, 13)
        h = (h * 5 + 0xE6546B64) & MASK
    tail = buf[len(buf) - len(buf) % 4:]
    if tail:
        k = int.from_bytes(tail, 'little')
        k = (k * 0xCC9E2D51) & MASK
        h ^= (_rotl(k, 15) * 0x1B873593) & MASK
    h ^= len(buf)
    return _fmix(h)


__all__ = ['murmur3_32']
