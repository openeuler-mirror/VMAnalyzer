"""File descriptor leak detection for long running guests.

A descriptor count that keeps rising and never drops indicates a leak, which
eventually hits the process limit and breaks unrelated code paths.
"""
import logging

LOG = logging.getLogger(__name__)


def growth_per_hour(values, interval_seconds):
    """Return the descriptor growth rate per hour across a series."""
    clean = [int(v) for v in values or []]
    if len(clean) < 2 or interval_seconds <= 0:
        LOG.debug('need at least two samples and a positive interval')
        return 0.0
    span_hours = interval_seconds * (len(clean) - 1) / 3600.0
    if span_hours <= 0:
        return 0.0
    return round((clean[-1] - clean[0]) / span_hours, 3)


def is_leaking(values, interval_seconds, tolerance_per_hour=5.0):
    """Report whether descriptors grow steadily beyond the tolerance."""
    return growth_per_hour(values, interval_seconds) > tolerance_per_hour


def hours_to_limit(current, hard_limit, growth_rate_per_hour):
    """Estimate hours until the descriptor limit is reached, or None."""
    if growth_rate_per_hour <= 0 or current >= hard_limit:
        return None
    return round((hard_limit - current) / growth_rate_per_hour, 2)


__all__ = ['growth_per_hour', 'is_leaking', 'hours_to_limit']
