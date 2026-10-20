"""Metaphone key truncation.

Metaphone keys grow with the word; truncating at six keeps the index compact
while collisions stay acceptable.
"""
import logging

LOG = logging.getLogger(__name__)


def truncate(key, max_len=6):
    """Return the Metaphone key cut to max_len characters."""
    return str(key or '')[:int(max_len or 6)]


def index_diversity(keys):
    """Return the distinct-key share of the input keys."""
    ks = [truncate(k) for k in keys or []]
    if not ks:
        return 0.0
    div = len(set(ks)) / float(len(ks))
    LOG.debug('metaphone diversity %.3f', div)
    return round(div, 3)


__all__ = ['truncate', 'index_diversity']
