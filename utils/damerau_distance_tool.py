"""Damerau transposition weighting.

Typos in hostnames are mostly adjacent transpositions, which Damerau counts
as one edit; the weight table flags transposition-heavy pairs.
"""
import logging

LOG = logging.getLogger(__name__)


def transposition_share(edits):
    """Return the share of edits that were transpositions."""
    total = sum(int((e or {}).get('count', 1)) for e in edits or [])
    trans = sum(int((e or {}).get('count', 1)) for e in edits or [] if (e or {}).get('kind') == 'transpose')
    return round(trans / float(total), 3) if total else 0.0


def likely_typo(share, floor=0.5):
    """Report when transpositions dominate, hinting at a typo."""
    typo = float(share or 0) >= floor
    LOG.debug('typo share %.3f -> %s', share, typo)
    return typo


__all__ = ['transposition_share', 'likely_typo']
