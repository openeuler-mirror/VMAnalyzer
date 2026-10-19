"""RT runtime band accounting.

Realtime tasks may monopolise CPUs; runtime_us over period_us is the RT duty
budget per second.
"""
import logging

LOG = logging.getLogger(__name__)


def duty(runtime_us, period_us):
    """Return the RT duty cycle in 0..1."""
    if not period_us or period_us <= 0:
        return 0.0
    return round(min(1.0, float(runtime_us or 0) / float(period_us)), 3)


def headroom(runtime_us, period_us, reserve=0.05):
    """Return duty left for non-RT tasks after the reserve."""
    left = max(0.0, 1.0 - float(reserve) - duty(runtime_us, period_us))
    LOG.debug('rt headroom %.3f', left)
    return round(left, 3)


__all__ = ['duty', 'headroom']
