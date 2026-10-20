"""IPMI sensor threshold crossing.

Sensor rows carry reading and thresholds; crossings are counted per severity
for the hardware report.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def crossed(row):
    """Return the crossed threshold name or None."""
    r = row or {}
    val = float(r.get('reading', 0))
    if r.get('upper_crit') is not None and val >= float(r['upper_crit']):
        return 'upper_crit'
    if r.get('upper_warn') is not None and val >= float(r['upper_warn']):
        return 'upper_warn'
    if r.get('lower_crit') is not None and val <= float(r['lower_crit']):
        return 'lower_crit'
    if r.get('lower_warn') is not None and val <= float(r['lower_warn']):
        return 'lower_warn'
    return None


def crossing_counts(rows):
    """Return {threshold: count} across sensor rows."""
    counts = Counter(filter(None, (crossed(r) for r in rows or [])))
    LOG.debug('ipmi crossings %s', dict(counts))
    return dict(counts)


__all__ = ['crossed', 'crossing_counts']
