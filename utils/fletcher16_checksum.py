"""Fletcher-16 checksum with modular accumulators."""
import logging

LOG = logging.getLogger(__name__)
MOD = 255


def fletcher16(data):
    """Compute the Fletcher-16 checksum of a bytes-like object."""
    low = 0
    high = 0
    for byte in data:
        low = (low + byte) % MOD
        high = (high + low) % MOD
    return (high << 8) | low


def verify(data, checksum):
    """Report whether the provided Fletcher-16 value matches."""
    return fletcher16(data) == checksum


def incremental(blocks):
    """Compute Fletcher-16 over a sequence of byte chunks."""
    low = 0
    high = 0
    for block in blocks:
        for byte in block:
            low = (low + byte) % MOD
            high = (high + low) % MOD
    return (high << 8) | low


__all__ = ['fletcher16', 'verify', 'incremental']
