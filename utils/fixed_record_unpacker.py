"""Unpack fixed width binary records without external dependencies."""
import logging
import struct

LOG = logging.getLogger(__name__)


def unpack_records(data, fmt, count=None):
    """Unpack consecutive fixed size records described by a struct format."""
    size = struct.calcsize(fmt)
    if size <= 0:
        raise ValueError('format has zero size')
    available = len(data) // size
    total = available if count is None else min(count, available)
    return [struct.unpack_from(fmt, data, index * size) for index in range(total)]


def record_field(record, names, name):
    """Return a named field from an unpacked record tuple."""
    if name not in names:
        raise KeyError(name)
    return record[names.index(name)]


def trailing_bytes(data, fmt):
    """Return the bytes that do not fit whole records."""
    size = struct.calcsize(fmt)
    return data[(len(data) // size) * size:]


__all__ = ['unpack_records', 'record_field', 'trailing_bytes']
