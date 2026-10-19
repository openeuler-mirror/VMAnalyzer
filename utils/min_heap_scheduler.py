"""Min-heap based next-fire scheduling.

Timers live in a min-heap keyed by fire time; the heap property cost is one
sift per operation, summarised here for capacity planning.
"""
import logging
import math

LOG = logging.getLogger(__name__)


def sift_cost(timer_count):
    """Return the worst-case comparison count for one sift."""
    n = max(1, int(timer_count or 1))
    return int(math.ceil(math.log(n, 2)))


def batch_pop_cost(timer_count, batch):
    """Return the comparison count for popping a batch of timers."""
    cost = int(batch or 0) * sift_cost(timer_count)
    LOG.debug('heap batch pop cost %d', cost)
    return cost


__all__ = ['sift_cost', 'batch_pop_cost']
