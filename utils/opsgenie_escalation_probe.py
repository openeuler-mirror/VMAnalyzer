"""Opsgenie escalation audit.

Alerts bouncing past their first escalation level mean the owning team
did not respond; counting levels finds the noisiest policies.
"""
import logging

LOG = logging.getLogger(__name__)


def escalated_beyond(alerts, level=1):
    """Return alerts whose escalation level exceeds the threshold."""
    return [a for a in alerts or [] if int(a.get('level', 0)) > level]


def level_histogram(alerts):
    """Return {level: alert count}."""
    hist = {}
    for alert in alerts or []:
        lv = int(alert.get('level', 0))
        hist[lv] = hist.get(lv, 0) + 1
    LOG.debug('escalation histogram %s', hist)
    return hist


__all__ = ['escalated_beyond', 'level_histogram']
