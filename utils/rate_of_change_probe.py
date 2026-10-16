"""Rate of change measurement for slowly moving gauges.

Absolute values hide how fast a gauge is moving, so the per second derivative is
computed while protecting against a missing previous sample.
"""
import logging

LOG = logging.getLogger(__name__)


def per_second(values, interval_seconds):
    """Return the per second rate of change for every sample after the first."""
    clean = [float(v) for v in values or [] if v is not None]
    if len(clean) < 2 or interval_seconds <= 0:
        LOG.debug('need at least two samples and a positive interval')
        return []
    return [round((clean[i] - clean[i - 1]) / float(interval_seconds), 5)
            for i in range(1, len(clean))]


def acceleration(values, interval_seconds):
    """Return the change in rate of change across the series."""
    rates = per_second(values, interval_seconds)
    if len(rates) < 2 or interval_seconds <= 0:
        return 0.0
    span = float(interval_seconds) * (len(rates) - 1)
    return round((rates[-1] - rates[0]) / span, 6)


def movement_verdict(rate, flat_band=0.001):
    """Classify movement as flat, rising or falling."""
    if abs(rate) <= flat_band:
        return 'flat'
    return 'rising' if rate > 0 else 'falling'


__all__ = ['per_second', 'acceleration', 'movement_verdict']
