"""Ring buffer overwrite rate.

Metrics rings must outlive the dashboard interval; overwrite rate tells how
fast old samples disappear.
"""
import logging

LOG = logging.getLogger(__name__)


def overwrite_age_sec(capacity, rate_per_sec):
    """Return the age of the oldest retained sample."""
    if not rate_per_sec or rate_per_sec <= 0:
        return float('inf')
    return round(float(capacity or 0) / float(rate_per_sec), 1)


def covers_interval(capacity, rate_per_sec, interval_sec):
    """Report when the ring covers the dashboard interval."""
    ok = overwrite_age_sec(capacity, rate_per_sec) >= float(interval_sec or 0)
    LOG.debug('ring covers interval=%s', ok)
    return ok


__all__ = ['overwrite_age_sec', 'covers_interval']
