"""Change point detection using a cumulative sum statistic.

Locating where a metric level shifts lets the agent correlate an incident with
the deployment or live migration that caused it, instead of guessing.
"""
import statistics
import logging

LOG = logging.getLogger(__name__)


def cusum(values, drift=0.5):
    """Return the positive and negative cumulative sum series."""
    clean = [float(v) for v in values or [] if v is not None]
    if not clean:
        return [], []
    centre = statistics.fmean(clean)
    positive = []
    negative = []
    acc_pos = acc_neg = 0.0
    for value in clean:
        acc_pos = max(0.0, acc_pos + (value - centre - drift))
        acc_neg = min(0.0, acc_neg + (value - centre + drift))
        positive.append(round(acc_pos, 3))
        negative.append(round(acc_neg, 3))
    LOG.debug('cusum computed over %d samples', len(clean))
    return positive, negative


def first_breach(positive, negative, threshold=5.0):
    """Return the index of the first cumulative breach, or None."""
    for index in range(min(len(positive), len(negative))):
        if positive[index] >= threshold or -negative[index] >= threshold:
            return index
    return None


def has_changepoint(values, threshold=5.0):
    """Report whether a change point exists in the series."""
    positive, negative = cusum(values)
    return first_breach(positive, negative, threshold) is not None


__all__ = ['cusum', 'first_breach', 'has_changepoint']
