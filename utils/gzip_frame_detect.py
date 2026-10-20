"""Detect gzip framing without fully decompressing content."""
import logging
import struct

LOG = logging.getLogger(__name__)
MAGIC = bytes([0x1f, 0x8b])
FLAG_FTEXT = 0x01
FLAG_FHCRC = 0x02
FLAG_FEXTRA = 0x04


def is_gzip(data):
    """Report whether a buffer starts with the gzip magic bytes."""
    return len(data) >= 2 and data[:2] == MAGIC


def header_info(data):
    """Parse the fixed gzip header fields of a buffer."""
    if not is_gzip(data):
        return None
    if len(data) < 10:
        raise ValueError('truncated gzip header')
    method, flags, mtime = struct.unpack_from('<BBI', data, 2)
    return {
        'method': method,
        'flags': flags,
        'mtime': mtime,
        'has_extra': bool(flags & FLAG_FEXTRA),
        'has_name': bool(flags & FLAG_FTEXT),
        'has_header_crc': bool(flags & FLAG_FHCRC),
    }


def compression_method_name(method):
    """Return a human readable name for a gzip method byte."""
    return {8: 'deflate'}.get(method, 'unknown')


__all__ = ['is_gzip', 'header_info', 'compression_method_name']
