"""MurmurHash3 x86 32 bit reference implementation."""
import logging

LOG = logging.getLogger(__name__)
C1 = 0xCC9E2D51
C2 = 0x1B873593
MASK = 0xFFFFFFFF


def _rotl32(value, count):
    """Rotate a 32 bit value left by count bits."""
    value &= MASK
    return ((value << count) | (value >> (32 - count))) & MASK


def murmur3_32(data, seed=0):
    """Compute the MurmurHash3 x86 32 bit digest of a bytes-like object."""
    h1 = seed & MASK
    length = len(data)
    blocks = length // 4
    for index in range(blocks):
        chunk = int.from_bytes(data[index * 4:index * 4 + 4], 'little')
        k1 = (chunk * C1) & MASK
        k1 = _rotl32(k1, 15)
        k1 = (k1 * C2) & MASK
        h1 ^= k1
        h1 = _rotl32(h1, 13)
        h1 = (h1 * 5 + 0xE6546B64) & MASK
    tail = data[blocks * 4:]
    k1 = 0
    if len(tail) >= 3:
        k1 ^= tail[2] << 16
    if len(tail) >= 2:
        k1 ^= tail[1] << 8
    if len(tail) >= 1:
        k1 ^= tail[0]
        k1 = (k1 * C1) & MASK
        k1 = _rotl32(k1, 15)
        k1 = (k1 * C2) & MASK
        h1 ^= k1
    h1 ^= length
    h1 ^= h1 >> 16
    h1 = (h1 * 0x85EBCA6B) & MASK
    h1 ^= h1 >> 13
    h1 = (h1 * 0xC2B2AE35) & MASK
    h1 ^= h1 >> 16
    return h1 & MASK


__all__ = ['murmur3_32']
