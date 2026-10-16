"""Connection pool saturation statistics.

A pool that is fully checked out makes callers queue even when the backend is
healthy, so pool occupancy must be tracked separately from backend latency.
"""
import logging

LOG = logging.getLogger(__name__)


def occupancy(active, idle, maximum):
    """Return the in use, total and utilisation figures of a pool."""
    maximum = int(maximum)
    active = int(active)
    idle = int(idle)
    if maximum <= 0:
        LOG.debug('pool reports zero capacity')
        return {'utilisation': 0.0, 'in_use': active, 'size': active + idle}
    return {
        'in_use': active,
        'size': active + idle,
        'utilisation': round(min(1.0, (active + idle) / float(maximum)), 4),
    }


def wait_pressure(active, maximum):
    """Return the share of pool capacity currently checked out."""
    if int(maximum) <= 0:
        return 0.0
    return round(min(1.0, int(active) / float(int(maximum))), 4)


def exhaustion_verdict(active, maximum, threshold=0.95):
    """Classify a pool as healthy, busy or exhausted."""
    pressure = wait_pressure(active, maximum)
    if pressure >= threshold:
        return 'exhausted'
    if pressure >= threshold - 0.2:
        return 'busy'
    return 'healthy'


__all__ = ['occupancy', 'wait_pressure', 'exhaustion_verdict']
