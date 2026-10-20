"""Trie fan-out analysis.

Prefix indexes blow up when one node carries most children; fan-out per depth
is summarised to spot the hot branch.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def depth_fanout(words):
    """Return {depth: max fan-out at that depth} for the word list."""
    fan = Counter()
    for w in words or []:
        seen = set()
        for depth in range(1, len(str(w)) + 1):
            prefix = str(w)[:depth]
            if prefix not in seen:
                seen.add(prefix)
                fan[depth] += 1
    LOG.debug('trie fanout depths=%d', len(fan))
    return dict(fan)


def share_at_depth(words, depth):
    """Return the largest single-prefix share of words at a depth."""
    c = Counter(str(w)[:depth] for w in words or [] if len(str(w)) >= depth)
    total = sum(c.values())
    return round(max(c.values()) / float(total), 3) if total else 0.0


__all__ = ['depth_fanout', 'share_at_depth']
