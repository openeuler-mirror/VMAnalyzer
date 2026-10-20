"""Estimate pace from position and elapsed time.

Turns a completed amount and an elapsed duration into a rate and a projected
finish time, tolerating zero elapsed time without dividing by zero.
"""
import logging

LOG = logging.getLogger(__name__)


def pace(completed, elapsed_seconds):
    """Return units completed per second, or zero when no time passed."""
    if elapsed_seconds <= 0:
        return 0.0
    return completed / float(elapsed_seconds)


def seconds_per_unit(elapsed_seconds, completed):
    """Return the average seconds needed per completed unit."""
    if completed <= 0:
        return None
    return elapsed_seconds / float(completed)


def projected_completion(total, completed, elapsed_seconds):
    """Return the estimated remaining seconds to finish the total."""
    rate = pace(completed, elapsed_seconds)
    if rate <= 0:
        return None
    return max(0.0, (total - completed) / rate)


__all__ = ["pace", "seconds_per_unit", "projected_completion"]
