"""Sliding window log limiter memory.

Storing every timestamp per key is exact but heavy; the memory per key is the
window times the peak rate times the entry size.
"""
import logging

LOG = logging.getLogger(__name__)


def entries_per_key(window_sec, peak_rate):
    """Return the worst-case timestamp count kept per key."""
    return int(float(window_sec or 0) * float(peak_rate or 0)) + 1


def memory_bytes(keys, window_sec, peak_rate, entry_size=16):
    """Return total limiter memory across keys."""
    total = int(keys or 0) * entries_per_key(window_sec, peak_rate) * int(entry_size or 16)
    LOG.debug('sliding log needs %d bytes', total)
    return total


__all__ = ['entries_per_key', 'memory_bytes']
