"""QEMU process thread census.

Runaway thread counts in qemu usually mean a misbehaving device model, so
per process thread totals are compared against a baseline.
"""
import logging

LOG = logging.getLogger(__name__)


def total_threads(thread_counts):
    """Return the summed thread count across processes."""
    return sum(int(c) for c in (thread_counts or []) if c is not None)


def outliers(thread_counts, watermark=64):
    """Return (pid, count) pairs whose thread count crosses the watermark."""
    hot = [(pid, int(c)) for pid, c in (thread_counts or {}).items() if int(c) >= watermark]
    LOG.debug('%d qemu processes over watermark', len(hot))
    return sorted(hot, key=lambda kv: -kv[1])


__all__ = ['total_threads', 'outliers']
