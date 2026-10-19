"""Context switch rate analysis.

A sudden switch rate jump usually means lock contention inside the guest, so
the current rate is compared against a rolling baseline.
"""
import logging
import statistics

LOG = logging.getLogger(__name__)


def rate(samples, interval_sec=60.0):
    """Return switches per second from cumulative counter samples."""
    clean = [float(s) for s in samples or [] if s is not None]
    if len(clean) < 2 or interval_sec <= 0:
        return 0.0
    span = float(interval_sec) * (len(clean) - 1)
    return round((clean[-1] - clean[0]) / span, 1)


def anomaly_factor(current_rate, baseline_rates):
    """Return current rate divided by the median baseline rate."""
    base = [float(b) for b in baseline_rates or [] if b and b > 0]
    if not base or current_rate <= 0:
        return 1.0
    factor = float(current_rate) / statistics.median(base)
    LOG.debug('ctx switch anomaly x%.2f', factor)
    return round(factor, 2)


__all__ = ['rate', 'anomaly_factor']
