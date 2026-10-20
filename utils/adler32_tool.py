"""Adler-32 checksum.

zlib wraps deflate with Adler-32; two running sums make it fast but only
suitable for short messages.
"""
import logging

LOG = logging.getLogger(__name__)
MOD = 65521


def adler32(data, seed=1):
    """Return the Adler-32 checksum of bytes-like data."""
    a, b = seed & 0xFFFF, (seed >> 16) & 0xFFFF
    for byte in bytes(data):
        a = (a + byte) % MOD
        b = (b + a) % MOD
    value = (b << 16) | a
    LOG.debug('adler32=%08x', value)
    return value


def verify_chunk(payload, expected):
    """Return True when the payload checksum matches expected."""
    return adler32(payload) == (int(expected) & 0xFFFFFFFF)


__all__ = ['adler32', 'verify_chunk', 'MOD']
