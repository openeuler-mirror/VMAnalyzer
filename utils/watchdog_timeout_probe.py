"""Watchdog expiry analysis.

A watchdog that fires during normal load means the timeout is too tight or
the guest stalls; firing intervals are summarised for tuning.
"""
import logging

LOG = logging.getLogger(__name__)


def mean_interval(fire_timestamps):
    """Return the mean seconds between consecutive watchdog fires."""
    stamps = sorted(float(t) for t in fire_timestamps or [])
    if len(stamps) < 2:
        return None
    gaps = [b - a for a, b in zip(stamps, stamps[1:])]
    return round(sum(gaps) / float(len(gaps)), 2)


def fires_per_hour(fire_timestamps, window_sec=3600.0):
    """Return the fire rate inside the trailing window."""
    stamps = sorted(float(t) for t in fire_timestamps or [])
    if len(stamps) < 2:
        return 0.0
    span = stamps[-1] - stamps[0]
    if span <= 0:
        return float(len(stamps))
    rate = (len(stamps) - 1) / span * float(window_sec)
    LOG.debug('watchdog %.2f fires/hour', rate)
    return round(rate, 2)


__all__ = ['mean_interval', 'fires_per_hour']
