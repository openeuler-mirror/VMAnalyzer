"""kdump vmcore size estimation.

A dump larger than its target partition is silently truncated, so the
expected vmcore size is compared against free space before a crash happens.
"""
import logging

LOG = logging.getLogger(__name__)


def estimate_vmcore_bytes(ram_bytes, compression_ratio=0.4):
    """Estimate the vmcore size from RAM size and compression ratio."""
    if ram_bytes <= 0:
        return 0
    return int(float(ram_bytes) * max(0.05, min(1.0, float(compression_ratio))))


def fits_target(ram_bytes, free_bytes, compression_ratio=0.4, headroom=1.2):
    """Report whether the dump fits with the required headroom."""
    need = estimate_vmcore_bytes(ram_bytes, compression_ratio) * float(headroom)
    ok = need <= float(free_bytes)
    LOG.debug('vmcore needs %.0f has %s', need, free_bytes)
    return ok


__all__ = ['estimate_vmcore_bytes', 'fits_target']
