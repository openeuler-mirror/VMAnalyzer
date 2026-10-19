"""API key rotation age probe.

Keys older than the rotation policy invite abuse; converting creation
timestamps to ages ranks the stalest keys.
"""
import logging
import time

LOG = logging.getLogger(__name__)


def key_age_days(created_ts, now=None):
    """Return key age in whole days."""
    now = time.time() if now is None else now
    return max(0, int((now - float(created_ts)) // 86400))


def overdue_keys(keys, max_age_days=90, now=None):
    """Return key ids older than max_age_days, stalest first."""
    now = time.time() if now is None else now
    aged = [(k.get('id'), key_age_days(k.get('created_ts', now), now))
            for k in keys or []]
    overdue = [pair for pair in aged if pair[1] > max_age_days]
    overdue.sort(key=lambda kv: kv[1], reverse=True)
    LOG.debug('overdue keys %d', len(overdue))
    return overdue


__all__ = ['key_age_days', 'overdue_keys']
