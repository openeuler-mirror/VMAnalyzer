"""qemu-guest-agent heartbeat freshness.

The agent channel is the only in-band management path, so a stale heartbeat
escalates quickly from warning to critical.
"""
import logging
import time

LOG = logging.getLogger(__name__)


def age_seconds(last_seen_ts, now=None):
    """Return how long ago the heartbeat was seen."""
    moment = time.time() if now is None else float(now)
    return round(max(0.0, moment - float(last_seen_ts)), 1)


def freshness(last_seen_ts, warn_sec=120.0, crit_sec=600.0, now=None):
    """Classify the heartbeat as fresh, stale or dead."""
    age = age_seconds(last_seen_ts, now)
    LOG.debug('guest agent age %.1fs', age)
    if age >= crit_sec:
        return 'dead'
    if age >= warn_sec:
        return 'stale'
    return 'fresh'


__all__ = ['age_seconds', 'freshness']
