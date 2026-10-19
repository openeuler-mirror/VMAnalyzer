"""Balloon driver inflation rate tracking.

Aggressive balloon inflation can push a guest into swap; tracking pages per
second lets the agent warn before the guest is starved.
"""
import logging

LOG = logging.getLogger(__name__)


def inflation_rate(samples, interval_sec=60.0):
    """Return pages per second gained by the balloon between two samples."""
    if len(samples or []) < 2 or interval_sec <= 0:
        return 0.0
    delta = float(samples[-1]) - float(samples[0])
    span = float(interval_sec) * (len(samples) - 1)
    return round(delta / span, 2)


def reclaim_eta(current_pages, target_pages, rate_per_sec):
    """Return seconds to reach the target at the current rate, or None."""
    if rate_per_sec <= 0:
        return None
    gap = float(target_pages) - float(current_pages)
    if gap <= 0:
        return 0.0
    eta = gap / rate_per_sec
    LOG.debug('balloon eta %.1fs', eta)
    return round(eta, 1)


__all__ = ['inflation_rate', 'reclaim_eta']
