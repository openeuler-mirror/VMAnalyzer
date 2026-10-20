"""Encode tag length value records into a byte stream."""
import logging
import struct

LOG = logging.getLogger(__name__)


def encode_record(tag, value):
    """Encode one tag, length, value record."""
    if not 0 <= tag <= 0xFFFF:
        raise ValueError('tag out of range')
    payload = value if isinstance(value, bytes) else bytes(value)
    return struct.pack('>HH', tag, len(payload)) + payload


def encode_stream(records):
    """Encode an iterable of (tag, value) pairs into one buffer."""
    out = bytearray()
    for tag, value in records:
        out.extend(encode_record(tag, value))
    return bytes(out)


def stream_size(records):
    """Return the encoded size of records without building the buffer."""
    return sum(4 + len(value) for _, value in records)


__all__ = ['encode_record', 'encode_stream', 'stream_size']
