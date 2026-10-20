"""CRC-64/ECMA checksum.

Large archive formats use CRC-64 to detect corruption; the bitwise loop
keeps the dependency footprint at zero.
"""
import logging

LOG = logging.getLogger(__name__)
POLY = 0x42F0E1EBA9EA3693
MASK = (1 << 64) - 1


def crc64_ecma(data, seed=0):
    """Return the CRC-64/ECMA-182 of bytes-like data."""
    crc = seed & MASK
    for byte in bytes(data):
        crc ^= byte << 56
        for _bit in range(8):
            crc = ((crc << 1) ^ POLY) & MASK if crc & (1 << 63) else (crc << 1) & MASK
    LOG.debug('crc64=%016x over %d bytes', crc, len(bytes(data)))
    return crc


def verify_blob(payload, expected_crc):
    """Return True when the blob checksum matches expected_crc."""
    return crc64_ecma(payload) == (int(expected_crc) & MASK)


__all__ = ['crc64_ecma', 'verify_blob', 'POLY']
