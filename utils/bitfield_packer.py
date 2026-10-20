"""Pack and unpack small integer fields into bit positions."""
import logging

LOG = logging.getLogger(__name__)


def pack_fields(fields):
    """Pack (value, width) pairs into one integer, low bits first."""
    result = 0
    shift = 0
    for value, width in fields:
        if value < 0 or value >= (1 << width):
            raise ValueError('value does not fit in width')
        result |= value << shift
        shift += width
    return result


def unpack_fields(value, widths):
    """Split an integer into a list of fields given their widths."""
    result = []
    shift = 0
    for width in widths:
        mask = (1 << width) - 1
        result.append((value >> shift) & mask)
        shift += width
    return result


def field_slice(value, offset, width):
    """Extract a single bit field at a given offset and width."""
    return (value >> offset) & ((1 << width) - 1)


__all__ = ['pack_fields', 'unpack_fields', 'field_slice']
