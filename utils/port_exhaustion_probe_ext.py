"""Ephemeral port exhaustion tracking.

Outgoing connections fail once the ephemeral range is fully allocated, so the
in-use count is tracked against the range size.
"""
import logging

LOG = logging.getLogger(__name__)


def in_use_ratio(in_use, range_start=32768, range_end=60999):
    """Return 0..1 usage of the ephemeral range."""
    size = max(1, int(range_end) - int(range_start))
    return round(max(0.0, min(1.0, float(in_use) / float(size))), 3)


def verdict(in_use, range_start=32768, range_end=60999, warn=0.7, crit=0.9):
    """Classify usage as ok, warn or crit."""
    ratio = in_use_ratio(in_use, range_start, range_end)
    LOG.debug('ephemeral ports %.1f%% used', ratio * 100)
    if ratio >= crit:
        return 'crit'
    if ratio >= warn:
        return 'warn'
    return 'ok'


__all__ = ['in_use_ratio', 'verdict']
