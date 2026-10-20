"""EDAC memory error tally.

Correctable errors accumulate before a DIMM fails; per-rank counts rank the
riskiest memory.
"""
import logging

LOG = logging.getLogger(__name__)


def rank_scores(rank_rows):
    """Return {rank: ce*1 + ue*10} risk scores."""
    scores = {}
    for rank, row in (rank_rows or {}).items():
        r = row or {}
        scores[rank] = int(r.get('ce', 0)) + 10 * int(r.get('ue', 0))
    return scores


def riskiest_rank(rank_rows):
    """Return the rank with the highest error score."""
    scores = rank_scores(rank_rows)
    best = max(scores.items(), key=lambda kv: kv[1], default=(None, 0))
    LOG.debug('edac riskiest rank %s score %d', best[0], best[1])
    return best[0]


__all__ = ['rank_scores', 'riskiest_rank']
