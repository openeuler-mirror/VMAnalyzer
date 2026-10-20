"""Ceph OSD membership probe.

An OSD that is down or out serves no data; counting both dimensions
shows how close the cluster is to losing redundancy.
"""
import logging

LOG = logging.getLogger(__name__)


def osd_summary(osds):
    """Return counts for up/down and in/out across OSD dicts."""
    summary = {'up': 0, 'down': 0, 'in': 0, 'out': 0}
    for osd in osds or []:
        summary['up' if osd.get('up') else 'down'] += 1
        summary['in' if osd.get('in') else 'out'] += 1
    return summary


def degraded(osds, max_down_ratio=0.05):
    """Return True when down OSDs exceed the allowed ratio."""
    summary = osd_summary(osds)
    total = summary['up'] + summary['down']
    ratio = 0.0 if total == 0 else summary['down'] / float(total)
    LOG.debug('ceph down ratio %.3f', ratio)
    return ratio > max_down_ratio


__all__ = ['osd_summary', 'degraded']
