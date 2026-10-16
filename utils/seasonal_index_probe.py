"""Seasonal index computation for periodic load patterns.

Dividing each period by the series mean expresses the periodic component, so
capacity planning can compare like for like hours.
"""
import logging

LOG = logging.getLogger(__name__)


def seasonal_indices(values):
    """Return each value expressed as a ratio of the series mean."""
    clean = [float(v) for v in values or [] if v is not None]
    if not clean:
        LOG.debug('empty series, no seasonal index')
        return []
    mean = sum(clean) / len(clean)
    if mean == 0:
        return [0.0] * len(clean)
    return [round(value / mean, 4) for value in clean]


def peak_index(values):
    """Return the largest seasonal index in the series."""
    indices = seasonal_indices(values)
    return max(indices) if indices else 0.0


def peak_verdict(values, strong=1.5, mild=1.15):
    """Classify the observed periodicity as strong, mild or flat."""
    peak = peak_index(values)
    if peak >= strong:
        return 'strong'
    if peak >= mild:
        return 'mild'
    return 'flat'


__all__ = ['seasonal_indices', 'peak_index', 'peak_verdict']
