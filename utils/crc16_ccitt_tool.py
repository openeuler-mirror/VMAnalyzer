"""CRC-16/CCITT checksum.

Modbus and X.25 frames carry this checksum; the bitwise form needs no
lookup table and works on tiny inputs.
"""
import logging

LOG = logging.getLogger(__name__)
POLY = 0x1021


def crc16_ccitt(data, seed=0xFFFF):
    """Return the CRC-16/CCITT of bytes-like data."""
    crc = seed & 0xFFFF
    for byte in bytes(data):
        crc ^= byte << 8
        for _bit in range(8):
            crc = ((crc << 1) ^ POLY) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    LOG.debug('crc16=%04x over %d bytes', crc, len(bytes(data)))
    return crc


def verify_frame(payload, expected_crc):
    """Return True when the payload checksum matches expected_crc."""
    return crc16_ccitt(payload) == (int(expected_crc) & 0xFFFF)


__all__ = ['crc16_ccitt', 'verify_frame', 'POLY']
