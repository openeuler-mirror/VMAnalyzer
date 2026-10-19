"""NFS server thread pool utilisation.

When all nfsd threads are busy, clients stall; utilisation is the busy share
of the configured thread count.
"""
import logging

LOG = logging.getLogger(__name__)


def utilisation(busy_threads, total_threads):
    """Return the busy share of nfsd threads in 0..1."""
    if not total_threads or total_threads <= 0:
        return 0.0
    return round(min(1.0, max(0.0, float(busy_threads or 0) / float(total_threads))), 3)


def saturated(util, ceiling=0.9):
    """Report when utilisation crossed the saturation ceiling."""
    sat = util >= ceiling
    if sat:
        LOG.warning('nfsd saturated util=%.3f', util)
    return sat


__all__ = ['utilisation', 'saturated']
