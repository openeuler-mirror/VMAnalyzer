"""Estimate drift between two clocks.

Given paired readings of a local and a remote clock the helper derives an
offset and a drift rate, which exposes clocks that wander instead of merely
disagreeing.
"""
import logging

LOG = logging.getLogger(__name__)


def offset(samples):
    """Return the smallest observed remote-minus-local offset."""
    if not samples:
        return 0.0
    return min(remote - local for local, remote in samples)


def drift_rate(samples):
    """Return offset change per second across the sample span."""
    ordered = sorted(samples)
    if len(ordered) < 2:
        return 0.0
    first_local, first_remote = ordered[0]
    last_local, last_remote = ordered[-1]
    span = last_local - first_local
    if span <= 0:
        return 0.0
    return ((last_remote - first_remote) - span) / span


def needs_correction(samples, limit_seconds):
    """Report whether the residual offset exceeds the limit."""
    return abs(offset(samples)) > limit_seconds


__all__ = ["offset", "drift_rate", "needs_correction"]
