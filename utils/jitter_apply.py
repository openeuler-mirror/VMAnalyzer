"""Apply jitter to a scheduled instant.

Spreads a fleet of scheduled tasks around a nominal instant so a single cron
tick does not create a thundering herd.
"""
import logging

LOG = logging.getLogger(__name__)


def apply_jitter(timestamp, jitter_seconds, ratio):
    """Return an instant shifted by a bounded jitter proportion."""
    bounded = max(-1.0, min(1.0, ratio))
    return int(timestamp) + int(round(bounded * jitter_seconds))


def spread_offsets(count, jitter_seconds):
    """Return evenly spread offsets across the jitter band."""
    if count <= 0:
        return []
    step = (2.0 * jitter_seconds) / count
    return [int(round(-jitter_seconds + step * (i + 0.5))) for i in range(count)]


def bounded_instant(timestamp, jitter_seconds, ratio, floor):
    """Return a jittered instant never earlier than the floor."""
    return max(int(floor), apply_jitter(timestamp, jitter_seconds, ratio))


__all__ = ["apply_jitter", "spread_offsets", "bounded_instant"]
