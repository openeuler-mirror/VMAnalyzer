"""CRC-8 with the SMBus polynomial used by firmware tables."""
import logging

LOG = logging.getLogger(__name__)
POLY = 0x07
INIT = 0x00
TABLE = []


def _build_table():
    """Build the 256 entry CRC-8 lookup table on demand."""
    for byte in range(256):
        crc = byte
        for _ in range(8):
            crc = ((crc << 1) ^ POLY) & 0xFF if crc & 0x80 else (crc << 1) & 0xFF
        TABLE.append(crc)


def crc8(data, init=INIT):
    """Compute the CRC-8 SMBus checksum over a bytes-like object."""
    if not TABLE:
        _build_table()
    crc = init
    for byte in data:
        crc = TABLE[crc ^ byte]
    return crc


def verify(data, expected=None):
    """Return True when the trailing byte matches the computed checksum."""
    if not data:
        return False
    target = data[-1] if expected is None else expected
    return crc8(data[:-1]) == target


__all__ = ['crc8', 'verify']
