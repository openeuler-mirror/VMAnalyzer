"""Thread pool saturation analysis.

A pool whose queue grows while active threads stay pinned at the maximum is
saturated, whereas queue length alone can mislead when threads are idle.
"""
import logging

LOG = logging.getLogger(__name__)


def saturation(active, maximum, queued):
    """Return the thread utilisation and queue backlog figures."""
    maximum = int(maximum)
    active = int(active)
    if maximum <= 0:
        LOG.debug('pool has no configured threads')
        return {'utilisation': 0.0, 'queued': int(queued)}
    return {
        'utilisation': round(min(1.0, active / float(maximum)), 4),
        'queued': int(queued),
        'starved': active >= maximum and int(queued) > 0,
    }


def queue_growth(queued_series):
    """Return the net queue growth across a series of samples."""
    values = [int(v) for v in queued_series or []]
    if len(values) < 2:
        return 0
    return values[-1] - values[0]


def verdict(state, queue_tolerance=100):
    """Classify the pool as healthy, backlogged or saturated."""
    if state.get('starved'):
        return 'saturated'
    if state.get('queued', 0) > queue_tolerance:
        return 'backlogged'
    return 'healthy'


__all__ = ['saturation', 'queue_growth', 'verdict']
