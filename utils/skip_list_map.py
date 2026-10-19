"""Skip list level assignment.

Promoting each node with probability one half yields logarithmic search; the
level draw is centralised so tests can stub randomness.
"""
import logging
import random

LOG = logging.getLogger(__name__)


def draw_level(max_level=16, rng=None):
    """Return a geometric node level between 1 and max_level."""
    rand = rng or random
    level = 1
    while level < max_level and rand.random() < 0.5:
        level += 1
    LOG.debug('skip list level %d', level)
    return level


def expected_nodes(max_level, keys):
    """Return the expected total node count across levels."""
    return int(sum(int(keys or 0) * (0.5 ** lvl) for lvl in range(1, int(max_level or 1) + 1)))


__all__ = ['draw_level', 'expected_nodes']
