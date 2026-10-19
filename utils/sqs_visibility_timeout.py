"""SQS visibility timeout sizing.

In-flight messages reappear when processing outlives the timeout;
sizing the timeout from observed latency stops duplicate work.
"""
import logging

LOG = logging.getLogger(__name__)


def suggested_timeout(processing_seconds, factor=1.5, floor=30, cap=43200):
    """Return a timeout covering processing time with headroom."""
    base = max(float(max(processing_seconds or [0])), 1.0)
    value = min(cap, max(floor, int(base * factor)))
    LOG.debug('suggested visibility timeout %ds', value)
    return value


def expired_inflight(messages, now):
    """Return messages whose visibility deadline already passed."""
    return [m for m in messages or []
            if float(m.get('visible_at', 0)) <= float(now)]


__all__ = ['suggested_timeout', 'expired_inflight']
