"""NTP synchronisation drift analysis.

A drifting clock breaks log ordering and token validity, so the offset and its
growth between polls are both tracked.
"""
import logging

LOG = logging.getLogger(__name__)


def offset_drift(offsets_ms, interval_seconds):
    """Return the clock offset drift rate in milliseconds per hour."""
    clean = [float(o) for o in offsets_ms or [] if o is not None]
    if len(clean) < 2 or interval_seconds <= 0:
        LOG.debug('insufficient offset samples for a drift estimate')
        return 0.0
    span_hours = interval_seconds * (len(clean) - 1) / 3600.0
    if span_hours <= 0:
        return 0.0
    return round((clean[-1] - clean[0]) / span_hours, 4)


def is_synchronised(offset_ms, tolerance_ms=100.0):
    """Report whether the clock offset stays inside tolerance."""
    return abs(float(offset_ms)) <= tolerance_ms


def drift_verdict(offsets_ms, interval_seconds, tolerant=50.0, bad=500.0):
    """Classify clock drift as locked, drifting or unsynchronised."""
    rate = abs(offset_drift(offsets_ms, interval_seconds))
    if rate >= bad:
        return 'unsynchronised'
    if rate >= tolerant:
        return 'drifting'
    return 'locked'


__all__ = ['offset_drift', 'is_synchronised', 'drift_verdict']
