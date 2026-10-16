"""Virtio balloon target versus actual inflation tracking.

The host asks the balloon driver to inflate or deflate, and a persistent gap
between the requested and achieved size means the guest cannot release memory.
"""
import logging

LOG = logging.getLogger(__name__)


def deviation(target_mb, actual_mb):
    """Return the absolute deviation between requested and achieved size."""
    return round(abs(float(target_mb) - float(actual_mb)), 3)


def convergence_ratio(target_mb, actual_mb):
    """Return how closely the balloon matches its target, in the 0..1 range."""
    target = float(target_mb)
    if target <= 0:
        LOG.debug('balloon target is not positive')
        return 1.0
    return round(max(0.0, 1.0 - abs(target - float(actual_mb)) / target), 4)


def balloon_verdict(target_mb, actual_mb, tolerance=32.0):
    """Classify balloon convergence as converged, lagging or stuck."""
    gap = deviation(target_mb, actual_mb)
    if gap <= tolerance:
        return 'converged'
    if gap <= tolerance * 4:
        return 'lagging'
    return 'stuck'


__all__ = ['deviation', 'convergence_ratio', 'balloon_verdict']
