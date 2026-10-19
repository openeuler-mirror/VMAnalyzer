"""Swap device priority planning.

Faster swap devices should drain first, so priorities are assigned from
measured latency tiers.
"""
import logging

LOG = logging.getLogger(__name__)


def tier_of(latency_ms):
    """Return a latency tier 0 (fast) to 2 (slow)."""
    ms = float(latency_ms or 0)
    if ms < 1.0:
        return 0
    if ms < 10.0:
        return 1
    return 2


def assign_priorities(devices):
    """Return name -> priority with the fastest device highest."""
    out = {}
    for name, latency_ms in (devices or {}).items():
        out[name] = 10 - 3 * tier_of(latency_ms)
    LOG.debug('swap priorities %s', out)
    return out


__all__ = ['tier_of', 'assign_priorities']
