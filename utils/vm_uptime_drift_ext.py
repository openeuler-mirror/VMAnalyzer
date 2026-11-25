"""Guest versus host uptime drift.

A guest clock that drifts from its uptime counter signals heavy steal or a
broken clocksource, so the two counters are compared.
"""
import logging

LOG = logging.getLogger(__name__)


def drift_seconds(wall_seconds, uptime_seconds):
    """Return the signed difference between wall time and uptime."""
    return round(float(wall_seconds) - float(uptime_seconds), 3)


def drift_ppm(wall_seconds, uptime_seconds):
    """Return the drift expressed in parts per million of wall time."""
    if not wall_seconds or wall_seconds <= 0:
        return 0.0
    ppm = drift_seconds(wall_seconds, uptime_seconds) / float(wall_seconds) * 1e6
    LOG.debug('uptime drift %.1f ppm', ppm)
    return round(ppm, 1)


def exceeds(ppm, threshold_ppm=500.0):
    """Report whether the drift magnitude crosses the threshold."""
    return abs(ppm) >= threshold_ppm


__all__ = ['drift_seconds', 'drift_ppm', 'exceeds']
