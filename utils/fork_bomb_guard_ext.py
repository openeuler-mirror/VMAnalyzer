"""Fork rate guard.

Runaway forking exhausts pid space in seconds; the guard watches forks per
second and triggers before the system becomes unrecoverable.
"""
import logging

LOG = logging.getLogger(__name__)


def forks_per_sec(counter_samples, interval_sec=60.0):
    """Return the fork rate from cumulative process counters."""
    clean = [float(s) for s in counter_samples or [] if s is not None]
    if len(clean) < 2 or interval_sec <= 0:
        return 0.0
    span = float(interval_sec) * (len(clean) - 1)
    return round((clean[-1] - clean[0]) / span, 2)


def should_throttle(counter_samples, limit_per_sec, interval_sec=60.0):
    """Report whether the fork rate must be throttled."""
    rate = forks_per_sec(counter_samples, interval_sec)
    if rate >= float(limit_per_sec):
        LOG.debug('fork rate %.1f/s over limit', rate)
        return True
    return False


__all__ = ['forks_per_sec', 'should_throttle']
