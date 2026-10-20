"""A dependency free 64 bit multiplicative hash in the xxHash spirit."""
import logging

LOG = logging.getLogger(__name__)
MASK = (1 << 64) - 1
PRIME1 = 0x9E3779B185EBCA87
PRIME2 = 0xC2B2AE3D27D4EB4F
PRIME3 = 0x165667B19E3779F9


def _mix(word):
    """Avalanche a single 64 bit word."""
    word = (word * PRIME2) & MASK
    word = ((word << 31) | (word >> 33)) & MASK
    return (word * PRIME3) & MASK


def hash64(data, seed=0):
    """Hash bytes into a well mixed 64 bit value."""
    acc = (seed + PRIME1) & MASK
    for byte in data:
        acc ^= _mix(byte + PRIME1)
        acc = ((acc << 27) | (acc >> 37)) & MASK
        acc = (acc * PRIME1 + PRIME3) & MASK
    acc ^= len(data)
    acc ^= acc >> 29
    acc = (acc * PRIME3) & MASK
    return (acc ^ (acc >> 32)) & MASK


__all__ = ['hash64']
