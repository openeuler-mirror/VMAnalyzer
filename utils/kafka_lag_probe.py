"""Kafka consumer lag scoring.

Lag per partition is log-end offset minus committed offset; the worst
partition decides whether the group is falling behind producers.
"""
import logging

LOG = logging.getLogger(__name__)


def partition_lags(end_offsets, committed_offsets):
    """Return {partition: end - committed} clamped at zero."""
    lags = {}
    for part, end in (end_offsets or {}).items():
        committed = (committed_offsets or {}).get(part, 0)
        lags[part] = max(0, int(end) - int(committed))
    return lags


def worst_partition(end_offsets, committed_offsets):
    """Return (partition, lag) with the largest lag."""
    lags = partition_lags(end_offsets, committed_offsets)
    worst = max(lags.items(), key=lambda kv: kv[1], default=(None, 0))
    LOG.debug('worst kafka lag partition=%s lag=%d', worst[0], worst[1])
    return worst


__all__ = ['partition_lags', 'worst_partition']
