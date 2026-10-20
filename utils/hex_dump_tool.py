"""Hex dump row formatter.

Binary fields in reports render as offset/hex/ascii rows of sixteen bytes;
this helper builds one canonical row.
"""
import logging

LOG = logging.getLogger(__name__)


def format_row(offset, chunk):
    """Return one canonical hex-dump row for up to 16 bytes."""
    data = bytes(chunk or b'')[:16]
    hexpart = ' '.join('%02x' % b for b in data)
    hexpart = hexpart.ljust(47)
    ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data)
    return '%08x  %s  |%s|' % (int(offset or 0), hexpart, ascii_part)


def row_count(total_bytes, width=16):
    """Return how many dump rows the blob needs."""
    n = (int(total_bytes or 0) + int(width or 16) - 1) // int(width or 16)
    LOG.debug('hex dump rows %d', n)
    return n


__all__ = ['format_row', 'row_count']
