"""Guard against non monotonic clock readings.

Wall clocks can step backwards when NTP corrects them, so durations must be
measured on a monotonic source and suspicious readings rejected.
"""
import logging

LOG = logging.getLogger(__name__)


def is_monotonic(previous, current):
    """Report whether a new reading is not older than the previous one."""
    return current >= previous


def safe_elapsed(previous, current, fallback=0.0):
    """Return a non negative elapsed time, falling back on clock steps."""
    if not is_monotonic(previous, current):
        LOG.warning("non monotonic clock step detected: %s -> %s", previous, current)
        return fallback
    return current - previous


def max_observed(values):
    """Return the running maximum of a sequence of readings."""
    peak = None
    for value in values:
        if peak is None or value > peak:
            peak = value
    return peak


__all__ = ["is_monotonic", "safe_elapsed", "max_observed"]
