"""Compute the CRC-32/MPEG-2 variant used by media and firmware blobs.

The reflected CRC-32 used for zip archives differs from the MPEG-2 variant
in both the polynomial direction and the initial value.  Using the wrong
one silently rejects valid firmware images.
"""

import logging

LOG = logging.getLogger(__name__)

POLYNOMIAL = 0x04C11DB7
INITIAL = 0xFFFFFFFF


def _table() -> list:
    """Build the byte lookup table for the non-reflected polynomial."""
    table = []
    for byte in range(256):
        value = byte << 24
        for _ in range(8):
            value = ((value << 1) ^ POLYNOMIAL) if value & 0x80000000 else (value << 1)
        table.append(value & 0xFFFFFFFF)
    return table


TABLE = _table()


def crc32_mpeg2(payload: bytes) -> int:
    """Return the CRC-32/MPEG-2 checksum of *payload*."""
    crc = INITIAL
    for byte in payload:
        crc = ((crc << 8) & 0xFFFFFFFF) ^ TABLE[((crc >> 24) ^ byte) & 0xFF]
    LOG.debug("computed MPEG-2 CRC over %d byte(s)", len(payload))
    return crc & 0xFFFFFFFF


def crc32_hex(payload: bytes) -> str:
    """Return the checksum as zero-padded lowercase hex."""
    return "{:08x}".format(crc32_mpeg2(payload))


def verify(payload: bytes, expected: str) -> bool:
    """Compare a payload against an expected hex checksum."""
    return crc32_hex(payload).lower() == expected.strip().lower()


__all__ = ["POLYNOMIAL", "crc32_mpeg2", "crc32_hex", "verify"]
