"""GCRA theoretical arrival time.

The generic cell rate algorithm stores one timestamp per key; the next
allowed arrival is the previous plus the emission interval.
"""
import logging

LOG = logging.getLogger(__name__)


def next_allowed(prev_tat, now, interval):
    """Return the new theoretical arrival time for a conforming cell."""
    return max(float(prev_tat or 0), float(now or 0)) + float(interval or 0)


def conforms(prev_tat, now, interval, burst):
    """Report whether a cell arriving now conforms to the limit."""
    ok = float(now or 0) + float(burst or 0) >= float(prev_tat or 0) - 0.0 or float(prev_tat or 0) <= float(now or 0)
    ok = float(now or 0) >= float(prev_tat or 0) - float(burst or 0)
    LOG.debug('gcra conforms=%s', ok)
    return ok


__all__ = ['next_allowed', 'conforms']
