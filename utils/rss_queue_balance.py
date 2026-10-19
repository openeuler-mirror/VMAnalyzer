"""RSS receive queue balance.

RSS should spread flows evenly across queues; the imbalance score compares the
busiest queue against the mean.
"""
import logging
import statistics

LOG = logging.getLogger(__name__)


def imbalance(packets_per_queue):
    """Return busiest queue divided by the mean, 1.0 when perfect."""
    counts = [max(0, int(c)) for c in packets_per_queue or []]
    if not counts:
        return 1.0
    mean = statistics.fmean(counts)
    if mean <= 0:
        return 1.0
    return round(max(counts) / mean, 3)


def starved_queues(packets_per_queue, ratio=0.2):
    """Return queue indices receiving less than ratio * mean traffic."""
    counts = [max(0, int(c)) for c in packets_per_queue or []]
    if not counts:
        return []
    mean = statistics.fmean(counts)
    cold = [i for i, c in enumerate(counts) if c < mean * ratio]
    LOG.debug('%d starved rss queues', len(cold))
    return cold


__all__ = ['imbalance', 'starved_queues']
