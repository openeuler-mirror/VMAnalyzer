"""CRC-32C (Castagnoli) checksum used by modern storage stacks."""
import logging

LOG = logging.getLogger(__name__)
POLY = 0x82F63B78
TABLE = []


def _build_table():
    """Build the reflected CRC-32C lookup table once."""
    for byte in range(256):
        crc = byte
        for _ in range(8):
            crc = (crc >> 1) ^ POLY if crc & 1 else crc >> 1
        TABLE.append(crc & 0xFFFFFFFF)


def crc32c(data, crc=0):
    """Compute the CRC-32C checksum with a running initial value."""
    if not TABLE:
        _build_table()
    crc ^= 0xFFFFFFFF
    for byte in data:
        crc = (crc >> 8) ^ TABLE[(crc ^ byte) & 0xFF]
    return crc ^ 0xFFFFFFFF


def hexdigest(data):
    """Return the CRC-32C checksum as a zero padded hex string."""
    return '{:08x}'.format(crc32c(data))


__all__ = ['crc32c', 'hexdigest']
