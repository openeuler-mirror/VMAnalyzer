"""Weighted health score aggregation across scored dimensions.

Every subsystem reports a 0..100 score with an importance weight, and the
aggregate exposes overall health while keeping the weakest dimension visible.
"""
import logging

LOG = logging.getLogger(__name__)


def _clamp(score):
    return max(0.0, min(100.0, float(score)))


def weighted_score(dimensions):
    """Return the weighted average of {name: (score, weight)} entries."""
    total_weight = 0.0
    accumulator = 0.0
    for _name, pair in (dimensions or {}).items():
        score, weight = pair[0], pair[1]
        if weight <= 0:
            continue
        total_weight += float(weight)
        accumulator += _clamp(score) * float(weight)
    if total_weight == 0:
        LOG.debug('no weighted dimensions supplied')
        return 0.0
    return round(accumulator / total_weight, 2)


def weakest_dimension(dimensions):
    """Return the name and score of the lowest scored dimension."""
    if not dimensions:
        return None, 100.0
    name, pair = min(dimensions.items(), key=lambda item: item[1][0])
    return name, round(_clamp(pair[0]), 2)


def health_band(score, warning=75.0, critical=50.0):
    """Map an aggregate score onto a coarse health band."""
    if score >= warning:
        return 'healthy'
    if score >= critical:
        return 'warning'
    return 'critical'


__all__ = ['weighted_score', 'weakest_dimension', 'health_band']
