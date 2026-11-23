"""ICMP echo latency trend.

Raw ping values are noisy, so the trend compares a recent window against an
older window of the same size.
"""
import logging
import statistics

LOG = logging.getLogger(__name__)


def trend_shift(samples, window=10):
    """Return recent median minus older median latency."""
    clean = [float(s) for s in samples or [] if s is not None]
    if len(clean) < window * 2:
        return 0.0
    old = statistics.median(clean[:window])
    new = statistics.median(clean[-window:])
    return round(new - old, 3)


def degrading(samples, window=10, tolerance_ms=5.0):
    """Report when latency rose by more than the tolerance."""
    shift = trend_shift(samples, window)
    LOG.debug('icmp shift %.3f ms', shift)
    return shift > tolerance_ms


__all__ = ['trend_shift', 'degrading']
