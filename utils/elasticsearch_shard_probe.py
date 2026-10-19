"""Elasticsearch shard allocation probe.

Unassigned shards mean missing data for queries; counting them by index
ranks which indices need allocation attention first.
"""
import logging

LOG = logging.getLogger(__name__)


def unassigned_by_index(shards):
    """Return {index: unassigned shard count}."""
    counts = {}
    for shard in shards or []:
        if shard.get('state') == 'UNASSIGNED':
            idx = shard.get('index', 'unknown')
            counts[idx] = counts.get(idx, 0) + 1
    return counts


def relocating_nodes(shards):
    """Return sorted node names that currently host relocating shards."""
    nodes = {s.get('node') for s in shards or [] if s.get('state') == 'RELOCATING'}
    LOG.debug('relocating nodes %s', sorted(n for n in nodes if n))
    return sorted(n for n in nodes if n)


__all__ = ['unassigned_by_index', 'relocating_nodes']
