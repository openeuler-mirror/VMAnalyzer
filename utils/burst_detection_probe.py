"""Burst detection over an event count series.

Traffic arriving in bursts stresses queues far more than its average rate
suggests, so peaks are compared against a quiet baseline.
"""
import statistics
import logging

LOG = logging.getLogger(__name__)


def burst_factor(counts, baseline_window=10):
    """Return the peak count divided by the median baseline."""
    clean = [float(c) for c in counts or [] if c is not None]
    if not clean:
        LOG.debug('empty series, no burst factor')
        return 0.0
    head = clean[:baseline_window]
    baseline = statistics.median(head) if head else 0.0
    if baseline <= 0:
        return 0.0
    return round(max(clean) / baseline, 3)


def burst_positions(counts, factor=3.0):
    """Return the indices whose count reaches the burst factor."""
    clean = [float(c) for c in counts or [] if c is not None]
    baseline = statistics.median(clean) if clean else 0.0
    if baseline <= 0:
        return []
    return [index for index, value in enumerate(clean) if value / baseline >= factor]


def burst_verdict(factor, strong=5.0, mild=2.0):
    """Classify burstiness as none, mild or strong."""
    if factor >= strong:
        return 'strong'
    if factor >= mild:
        return 'mild'
    return 'none'


__all__ = ['burst_factor', 'burst_positions', 'burst_verdict']
