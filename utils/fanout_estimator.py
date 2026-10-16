"""Estimation of fanout growth from a branching workload.

When one action triggers several downstream actions, the compounding effect
matters for capacity planning, so the growth curve is summarised.
"""
import logging

LOG = logging.getLogger(__name__)


def fanout_series(branching, depth):
    """Return the number of tasks at each level of a branching factor."""
    factor = float(branching)
    if factor <= 0 or depth < 0:
        raise ValueError('branching must be positive and depth non-negative')
    series = []
    level = 1.0
    for _ in range(int(depth) + 1):
        series.append(int(round(level)))
        level *= factor
    return series


def total_tasks(branching, depth):
    """Return the cumulative number of tasks across all levels."""
    return sum(fanout_series(branching, depth))


def saturation_level(branching, ceiling):
    """Return the first level whose task count exceeds the ceiling."""
    factor = float(branching)
    if factor <= 1:
        return 0
    level = 1.0
    index = 0
    while round(level) <= ceiling and index < 128:
        level *= factor
        index += 1
    LOG.debug('saturation reached at level %d', index)
    return index


__all__ = ['fanout_series', 'total_tasks', 'saturation_level']
