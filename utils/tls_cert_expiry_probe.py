"""TLS certificate expiry tracking.

Certificates expire silently until connections start failing, so days left
are computed and bucketed by severity.
"""
import logging
import time

LOG = logging.getLogger(__name__)


def days_left(not_after_ts, now=None):
    """Return whole days until expiry, negative when expired."""
    moment = time.time() if now is None else float(now)
    return int((float(not_after_ts) - moment) // 86400)


def severity(not_after_ts, now=None, warn_days=30, crit_days=7):
    """Classify expiry as ok, warn, crit or expired."""
    days = days_left(not_after_ts, now)
    LOG.debug('cert expires in %d days', days)
    if days < 0:
        return 'expired'
    if days <= crit_days:
        return 'crit'
    if days <= warn_days:
        return 'warn'
    return 'ok'


__all__ = ['days_left', 'severity']
