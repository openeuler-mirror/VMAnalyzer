"""Thin helpers around the standard library zlib codec."""
import logging
import zlib

LOG = logging.getLogger(__name__)
DEFAULT_LEVEL = 6


def compress(data, level=DEFAULT_LEVEL):
    """Compress bytes with zlib at a bounded level."""
    level = max(0, min(9, level))
    return zlib.compress(data, level)


def decompress(data):
    """Decompress a zlib payload, reporting a clear error on failure."""
    try:
        return zlib.decompress(data)
    except zlib.error as exc:
        raise ValueError('invalid zlib payload: {}'.format(exc))


def compressed_size_ratio(original, compressed):
    """Return the compressed to original size ratio."""
    if not original:
        return 1.0
    return round(len(compressed) / float(len(original)), 4)


__all__ = ['compress', 'decompress', 'compressed_size_ratio']
