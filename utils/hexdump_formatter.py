"""Format byte buffers into classic hex dump lines."""
import logging

LOG = logging.getLogger(__name__)
BYTES_PER_LINE = 16


def _printable(byte):
    """Return a printable representation for a single byte value."""
    return chr(byte) if 32 <= byte < 127 else '.'


def format_line(offset, chunk):
    """Render one offset addressed hex dump line."""
    hex_part = ' '.join('{:02x}'.format(byte) for byte in chunk)
    hex_part = hex_part.ljust(BYTES_PER_LINE * 3 - 1)
    ascii_part = ''.join(_printable(byte) for byte in chunk)
    return '{:08x}  {}  |{}|'.format(offset, hex_part, ascii_part)


def dump(data, base=0):
    """Return formatted dump lines for a bytes-like object."""
    lines = []
    for start in range(0, len(data), BYTES_PER_LINE):
        chunk = data[start:start + BYTES_PER_LINE]
        lines.append(format_line(base + start, chunk))
    if not lines:
        lines.append(format_line(base, b''))
    return lines


__all__ = ['format_line', 'dump']
