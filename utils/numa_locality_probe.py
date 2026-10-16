"""NUMA locality scoring from per node hit and miss counters.

A guest that touches memory far from its vCPU node pays a remote latency
penalty.  Locality is expressed as the local hit ratio so nodes can be ranked.
"""
import logging

LOG = logging.getLogger(__name__)


def locality_ratio(local_hits, remote_hits):
    """Return the fraction of accesses that hit the local NUMA node."""
    local = max(0, int(local_hits))
    remote = max(0, int(remote_hits))
    total = local + remote
    if total == 0:
        LOG.debug('no NUMA accesses recorded')
        return 0.0
    return round(local / float(total), 4)


def rank_nodes(node_stats):
    """Rank nodes by locality ratio, worst first, as (node, ratio) pairs."""
    ranked = []
    for node, stats in (node_stats or {}).items():
        ratio = locality_ratio(stats.get('local', 0), stats.get('remote', 0))
        ranked.append((node, ratio))
    return sorted(ranked, key=lambda item: item[1])


def imbalance_penalty(ratios):
    """Quantify how uneven locality is across nodes using the spread."""
    values = [r for r in ratios if r is not None]
    if len(values) < 2:
        return 0.0
    return round(max(values) - min(values), 4)


__all__ = ['locality_ratio', 'rank_nodes', 'imbalance_penalty']
