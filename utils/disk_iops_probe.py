"""Disk IOPS computation from cumulative block device counters.

devices expose cumulative read and write completions; dividing the delta by
the elapsed interval yields observed IOPS, which is what the guest actually
issues independent of the host backing store.
"""
import logging

LOG = logging.getLogger(__name__)


def iops(prev, curr, interval_sec):
    """Return read/write IOPS from two counter snapshots."""
    if interval_sec <= 0:
        LOG.warning('non positive interval, IOPS undefined')
        return {'read_iops': 0.0, 'write_iops': 0.0}
    return {
        'read_iops': round(max(0, curr.get('reads', 0) - prev.get('reads', 0)) / interval_sec, 2),
        'write_iops': round(max(0, curr.get('writes', 0) - prev.get('writes', 0)) / interval_sec, 2),
    }


def read_write_ratio(snapshot):
    """Return the read share of total completions in a snapshot."""
    reads = max(0, int(snapshot.get('reads', 0)))
    writes = max(0, int(snapshot.get('writes', 0)))
    total = reads + writes
    if total == 0:
        return 0.0
    return round(reads / float(total), 4)


def peak_iops(series):
    """Return the highest observed read+write IOPS across a series."""
    return max((s.get('read_iops', 0) + s.get('write_iops', 0) for s in series), default=0.0)


__all__ = ['iops', 'read_write_ratio', 'peak_iops']
