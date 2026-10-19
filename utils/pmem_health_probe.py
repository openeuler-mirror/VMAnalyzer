"""Persistent memory health snapshot.

NVDIMM health flags arrive as a bitmask; individual flags decide whether the
device keeps serving or needs replacement.
"""
import logging

LOG = logging.getLogger(__name__)

FLAG_SPARES_LOW = 0x1
FLAG_MEDIA_ERROR = 0x2
FLAG_DIRTY_SHUTDOWN = 0x4


def decode_flags(bitmask):
    """Return a dict of decoded pmem health flags."""
    mask = int(bitmask or 0)
    return {'spares_low': bool(mask & FLAG_SPARES_LOW),
            'media_error': bool(mask & FLAG_MEDIA_ERROR),
            'dirty_shutdown': bool(mask & FLAG_DIRTY_SHUTDOWN)}


def needs_replacement(bitmask):
    """Report when media errors or exhausted spares demand replacement."""
    flags = decode_flags(bitmask)
    bad = flags['spares_low'] or flags['media_error']
    if bad:
        LOG.warning('pmem replacement advised flags=%s', flags)
    return bad


__all__ = ['decode_flags', 'needs_replacement']
