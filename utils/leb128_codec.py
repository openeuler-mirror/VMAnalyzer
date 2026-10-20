"""Unsigned LEB128 variable length integer encoding."""
import logging

LOG = logging.getLogger(__name__)
CONTINUATION = 0x80
PAYLOAD = 0x7F


def encode_unsigned(value):
    """Encode a non negative integer as unsigned LEB128 bytes."""
    if value < 0:
        raise ValueError('value must be non negative')
    out = bytearray()
    while True:
        byte = value & PAYLOAD
        value >>= 7
        if value:
            out.append(byte | CONTINUATION)
        else:
            out.append(byte)
            return bytes(out)


def decode_unsigned(data, offset=0):
    """Decode an unsigned LEB128 integer, returning (value, next_offset)."""
    result = 0
    shift = 0
    index = offset
    while index < len(data):
        byte = data[index]
        result |= (byte & PAYLOAD) << shift
        index += 1
        if not byte & CONTINUATION:
            return result, index
        shift += 7
    raise ValueError('truncated LEB128 sequence')


def encoded_length(value):
    """Return how many bytes the unsigned LEB128 form needs."""
    length = 1
    value >>= 7
    while value:
        length += 1
        value >>= 7
    return length


__all__ = ['encode_unsigned', 'decode_unsigned', 'encoded_length']
