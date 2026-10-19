"""Quota soft-limit grace tracking.

Users may exceed soft quotas only during the grace window, so the over-soft
duration is compared to the configured grace period.
"""
import logging

LOG = logging.getLogger(__name__)


def grace_left(over_since_ts, now_ts, grace_sec):
    """Return remaining grace seconds, never negative."""
    elapsed = max(0.0, float(now_ts or 0) - float(over_since_ts or 0))
    return max(0.0, float(grace_sec or 0) - elapsed)


def enforce_now(over_since_ts, now_ts, grace_sec):
    """Report when the grace window expired and hard enforcement applies."""
    expired = grace_left(over_since_ts, now_ts, grace_sec) <= 0.0
    if expired:
        LOG.warning('quota grace expired, enforcing hard limit')
    return expired


__all__ = ['grace_left', 'enforce_now']
