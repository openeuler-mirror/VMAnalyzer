"""Per channel notification throttling.

Even a correct alert storm should not page a human more than a fixed number of
times per interval, so deliveries are counted per channel against a budget.
"""
import logging

LOG = logging.getLogger(__name__)


def throttle_state(history, channel, now, interval=600, limit=5):
    """Return the remaining delivery budget for a channel."""
    recent = [ts for ts in (history.get(channel) or []) if now - ts < interval]
    remaining = max(0, limit - len(recent))
    if remaining == 0:
        LOG.info('channel %s exhausted its notification budget', channel)
    return {'channel': channel, 'sent': len(recent), 'remaining': remaining}


def record_delivery(history, channel, now, interval=600):
    """Append a delivery stamp and prune entries older than the interval."""
    stamps = [ts for ts in (history.get(channel) or []) if now - ts < interval]
    stamps.append(now)
    history[channel] = stamps
    return len(stamps)


def may_notify(history, channel, now, interval=600, limit=5):
    """Report whether a channel may send another notification."""
    return throttle_state(history, channel, now, interval, limit)['remaining'] > 0


__all__ = ['throttle_state', 'record_delivery', 'may_notify']
