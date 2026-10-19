"""NetFlow record volume estimation.

Flow export volume grows with connection churn; records per second sizing
prevents the collector from being overwhelmed.
"""
import logging

LOG = logging.getLogger(__name__)


def records_per_sec(flows, interval_sec):
    """Return exported records per second."""
    if not interval_sec or interval_sec <= 0:
        return 0.0
    return round(float(flows) / float(interval_sec), 2)


def collector_load(records, capacity_per_sec):
    """Return 0..1 collector load for the offered rate."""
    if capacity_per_sec <= 0:
        return 0.0
    load = float(records) / float(capacity_per_sec)
    LOG.debug('netflow load %.2f', load)
    return round(min(1.0, max(0.0, load)), 3)


__all__ = ['records_per_sec', 'collector_load']
