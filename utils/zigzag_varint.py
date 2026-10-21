"""ZigZag mapping of signed integers onto unsigned varints."""
import logging

LOG = logging.getLogger(__name__)


def zigzag_encode(value):
    """Map a signed integer onto a non negative zigzag integer."""
    return (value << 1) ^ (value >> 63)


def zigzag_decode(value):
    """Recover the signed integer from a zigzag encoded value."""
    return (value >> 1) ^ -(value & 1)


def encode_signed(value):
    """Return the zigzag varint bytes for a signed integer."""
    mapped = zigzag_encode(value)
    out = bytearray()
    while True:
        chunk = mapped & 0x7F
        mapped >>= 7
        out.append(chunk | 0x80 if mapped else chunk)
        if not mapped:
            return bytes(out)


def decode_signed(data):
    """Decode a zigzag varint byte string back to a signed integer."""
    value = 0
    shift = 0
    for byte in data:
        value |= (byte & 0x7F) << shift
        shift += 7
    return zigzag_decode(value)


__all__ = ['zigzag_encode', 'zigzag_decode', 'encode_signed', 'decode_signed']
