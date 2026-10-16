"""LVM thin pool capacity projection.

Thin pools over commit storage, so the data percentage matters even when the
pool looks empty; exceeding it forces every volume read only.
"""
import logging

LOG = logging.getLogger(__name__)


def pool_usage(data_percent, metadata_percent):
    """Return the data and metadata usage of a thin pool."""
    return {
        'data': round(min(1.0, float(data_percent) / 100.0), 4),
        'metadata': round(min(1.0, float(metadata_percent) / 100.0), 4),
    }


def days_until_full(free_mb, growth_mb_per_day):
    """Estimate days until the thin pool is exhausted, or None."""
    if growth_mb_per_day <= 0:
        LOG.debug('pool growth is not positive, cannot project')
        return None
    return round(float(free_mb) / float(growth_mb_per_day), 2)


def thin_verdict(data_percent, metadata_percent, warn=80.0, crit=95.0):
    """Classify thin pool pressure as healthy, warning or critical."""
    worst = max(float(data_percent), float(metadata_percent))
    if worst >= crit:
        return 'critical'
    if worst >= warn:
        return 'warning'
    return 'healthy'


__all__ = ['pool_usage', 'days_until_full', 'thin_verdict']
