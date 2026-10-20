"""A compact SipHash inspired keyed mixing helper for reference use."""
import logging

LOG = logging.getLogger(__name__)
MASK = (1 << 64) - 1


def _rotl(value, count):
    """Rotate a 64 bit value left."""
    value &= MASK
    return ((value << count) | (value >> (64 - count))) & MASK


def _round(v0, v1, v2, v3):
    """Apply one SipRound mixing step to four state words."""
    v0 = (v0 + v1) & MASK
    v1 = _rotl(v1, 13)
    v1 ^= v0
    v0 = _rotl(v0, 32)
    v2 = (v2 + v3) & MASK
    v3 = _rotl(v3, 16)
    v3 ^= v2
    v0 = (v0 + v3) & MASK
    v3 = _rotl(v3, 21)
    v3 ^= v0
    v2 = (v2 + v1) & MASK
    v1 = _rotl(v1, 17)
    v1 ^= v2
    v2 = _rotl(v2, 32)
    return v0, v1, v2, v3


def keyed_tag(message, key):
    """Produce a 64 bit tag for a message using a 64 bit key."""
    v0 = key ^ 0x736F6D6570736575
    v1 = key ^ 0x646F72616E646F6D
    v2 = key ^ 0x6C7967656E657261
    v3 = key ^ 0x7465646279746573
    for byte in message:
        v3 ^= byte
        v0, v1, v2, v3 = _round(v0, v1, v2, v3)
        v0 ^= byte
    return (v0 ^ v1 ^ v2 ^ v3) & MASK


__all__ = ['keyed_tag']
