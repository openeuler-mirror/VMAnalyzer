"""systemd timer drift audit.

Timers with AccuracySec slack fire late under load; observed minus scheduled
delay measures the drift.
"""
import logging

LOG = logging.getLogger(__name__)


def drift_seconds(scheduled_ts, fired_ts):
    """Return how late the timer fired, never negative."""
    return max(0.0, float(fired_ts or 0) - float(scheduled_ts or 0))


def within_accuracy(drift, accuracy_sec):
    """Report whether the drift stayed inside AccuracySec."""
    ok = float(drift or 0) <= float(accuracy_sec or 0)
    if not ok:
        LOG.warning('timer drift %.1fs beyond accuracy %ss', drift, accuracy_sec)
    return ok


__all__ = ['drift_seconds', 'within_accuracy']
