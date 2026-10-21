"""Decode tag length value records from a byte stream."""
import logging
import struct

LOG = logging.getLogger(__name__)
HEADER_SIZE = 4


def decode_record(data, offset=0):
    """Decode a single record, returning (tag, value, next_offset)."""
    if offset + HEADER_SIZE > len(data):
        raise ValueError('truncated record header')
    tag, length = struct.unpack_from('>HH', data, offset)
    start = offset + HEADER_SIZE
    end = start + length
    if end > len(data):
        raise ValueError('record value exceeds buffer')
    return tag, bytes(data[start:end]), end


def decode_stream(data):
    """Decode every record in a buffer into (tag, value) tuples."""
    records = []
    offset = 0
    while offset < len(data):
        tag, value, offset = decode_record(data, offset)
        records.append((tag, value))
    return records


def find_tag(data, tag):
    """Return the first value with a matching tag, or None."""
    for record_tag, value in decode_stream(data):
        if record_tag == tag:
            return value
    return None


__all__ = ['decode_record', 'decode_stream', 'find_tag']
