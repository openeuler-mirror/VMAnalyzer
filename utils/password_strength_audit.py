"""Password strength scoring.

A length-plus-variety score rejects weak admin passwords without external
crack lists.
"""
import logging

LOG = logging.getLogger(__name__)


def variety_count(password):
    """Return how many of lower/upper/digit/symbol classes appear."""
    p = str(password or '')
    classes = [any(c.islower() for c in p), any(c.isupper() for c in p),
               any(c.isdigit() for c in p), any(not c.isalnum() for c in p)]
    return sum(1 for c in classes if c)


def score(password):
    """Return a 0..100 strength score from length and variety."""
    p = str(password or '')
    s = min(60, len(p) * 5) + variety_count(p) * 10
    LOG.debug('password score %d', s)
    return min(100, s)


__all__ = ['variety_count', 'score']
