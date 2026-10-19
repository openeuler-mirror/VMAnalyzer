"""ROC AUC from raw scores.

The Mann-Whitney rank statistic computes area under the ROC curve
without materializing the curve itself.
"""
import logging

LOG = logging.getLogger(__name__)


def auc(scores, labels):
    """Return the probability a random positive outranks a negative."""
    pairs = sorted(zip(scores or [], labels or []), key=lambda kv: kv[0])
    rank_sum = 0.0
    pos = neg = 0
    for rank, (_score, label) in enumerate(pairs, start=1):
        if label:
            rank_sum += rank
            pos += 1
        else:
            neg += 1
    if pos == 0 or neg == 0:
        return 0.0
    value = (rank_sum - pos * (pos + 1) / 2.0) / (pos * neg)
    LOG.debug('auc %.4f on %d pos / %d neg', value, pos, neg)
    return round(value, 4)


__all__ = ['auc']
