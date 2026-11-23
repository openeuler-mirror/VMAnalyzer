"""BGP peer state summarising.

Peers bouncing between states churn the routing table, so state dwell times
are aggregated per peer.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def state_counts(observations):
    """Return {state: observation_count} for one peer."""
    return dict(Counter(str(s) for s in observations or []))


def is_stable(observations, established_share=0.95):
    """Report when Established dominates the observation window."""
    counts = state_counts(observations)
    total = sum(counts.values())
    if total == 0:
        return True
    share = counts.get('Established', 0) / float(total)
    LOG.debug('bgp established share %.3f', share)
    return share >= established_share


__all__ = ['state_counts', 'is_stable']
