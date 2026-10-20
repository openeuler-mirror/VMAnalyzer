"""Inspect the first deflate block header of a raw stream."""
import logging

LOG = logging.getLogger(__name__)
BTYPE_NAMES = {0: 'stored', 1: 'fixed_huffman', 2: 'dynamic_huffman', 3: 'reserved'}


def read_bit(byte_value, position):
    """Return the bit at a zero based position within a byte."""
    return (byte_value >> position) & 1


def first_block_header(data):
    """Decode the BFINAL and BTYPE fields from the first deflate byte."""
    if not data:
        raise ValueError('empty deflate stream')
    first = data[0]
    bfinal = first & 1
    btype = (first >> 1) & 0x03
    return {'bfinal': bfinal, 'btype': btype, 'block_type': BTYPE_NAMES[btype]}


def describe(data):
    """Return a short textual description of the first deflate block."""
    header = first_block_header(data)
    final = 'final' if header['bfinal'] else 'continued'
    return '{} {} block'.format(final, header['block_type'])


__all__ = ['read_bit', 'first_block_header', 'describe']
