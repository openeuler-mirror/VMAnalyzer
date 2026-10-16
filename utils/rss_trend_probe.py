"""Resident set size trend estimation.

A monotone RSS slope across a run points at a leak, whereas a sudden step means
a configuration change, so slope and step are reported separately.
"""
import statistics
import logging

LOG = logging.getLogger(__name__)


def slope_per_hour(values, interval_seconds):
    """Return the least squares RSS slope expressed per hour."""
    clean = [float(v) for v in values or [] if v is not None]
    if len(clean) < 2 or interval_seconds <= 0:
        LOG.debug('insufficient data for a slope estimate')
        return 0.0
    xs = [index * interval_seconds / 3600.0 for index in range(len(clean))]
    mean_x = statistics.fmean(xs)
    mean_y = statistics.fmean(clean)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, clean))
    denominator = sum((x - mean_x) ** 2 for x in xs)
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 4)


def detects_step(values, ratio=1.5):
    """Report whether RSS jumped by the given ratio between two samples."""
    clean = [float(v) for v in values or [] if v is not None]
    for index in range(1, len(clean)):
        if clean[index - 1] > 0 and clean[index] / clean[index - 1] >= ratio:
            return True
    return False


def memory_verdict(slope_mb_per_hour, leak_threshold=20.0):
    """Classify an RSS slope as stable, growing or leaking."""
    if slope_mb_per_hour >= leak_threshold:
        return 'leaking'
    if slope_mb_per_hour > 0:
        return 'growing'
    return 'stable'


__all__ = ['slope_per_hour', 'detects_step', 'memory_verdict']
