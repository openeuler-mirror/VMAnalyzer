"""Capacity runway projection from a burn rate series.

Rather than alerting on an absolute threshold, the agent projects how long a
resource can sustain its current consumption before it is exhausted.
"""
import statistics
import logging

LOG = logging.getLogger(__name__)


def burn_rate(values):
    """Return the average per sample increase of a usage series."""
    clean = [float(v) for v in values or [] if v is not None]
    if len(clean) < 2:
        return 0.0
    deltas = [b - a for a, b in zip(clean, clean[1:])]
    return round(statistics.fmean(deltas), 4)


def runway_samples(values, ceiling=100.0):
    """Return how many samples remain until usage reaches the ceiling."""
    clean = [float(v) for v in values or [] if v is not None]
    if not clean:
        return 0
    rate = burn_rate(clean)
    if rate <= 0:
        return -1
    remaining = float(ceiling) - clean[-1]
    if remaining <= 0:
        return 0
    return int(remaining / rate)


def exhaustion_eta(values, interval_sec=60.0, ceiling=100.0):
    """Return seconds until exhaustion, or None when usage is not rising."""
    steps = runway_samples(values, ceiling)
    if steps < 0:
        LOG.debug('usage not rising, no exhaustion eta')
        return None
    return round(steps * float(interval_sec), 1)


__all__ = ['burn_rate', 'runway_samples', 'exhaustion_eta']
