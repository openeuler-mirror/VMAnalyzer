"""Varint length peeking.

Length-prefixed protocol frames start with a varint; its byte count is known
from the leading bits before decoding.
"""
import logging

LOG = logging.getLogger(__name__)


def encoded_len(value):
    """Return how many bytes the varint encoding of value occupies."""
    v = int(value or 0)
    if v < 0:
        raise ValueError('varint needs a non-negative value')
    n = 1
    while v >= 0x80:
        v >>= 7
        n += 1
    return n


def decode_len_field(data):
    """Return (value, bytes consumed) for the leading varint."""
    blob = bytes(data or b'')
    shift = 0
    value = 0
    for i, b in enumerate(blob[:10]):
        value |= (b & 0x7F) << shift
        if not b & 0x80:
            LOG.debug('varint %d in %d bytes', value, i + 1)
            return value, i + 1
        shift += 7
    return 0, 0


__all__ = ['encoded_len', 'decode_len_field']
