"""CRL next-update tracking.

An expired CRL makes revocation checks fail closed; days remaining decide the
alert level.
"""
import logging

LOG = logging.getLogger(__name__)


def days_left(next_update_ts, now_ts):
    """Return whole days until the CRL expires."""
    return int((float(next_update_ts or 0) - float(now_ts or 0)) / 86400.0)


def alert_level(days):
    """Return the alert level for the days remaining."""
    d = int(days or 0)
    level = 'ok' if d > 7 else 'warn' if d > 1 else 'crit'
    LOG.debug('crl days %d -> %s', d, level)
    return level


__all__ = ['days_left', 'alert_level']
