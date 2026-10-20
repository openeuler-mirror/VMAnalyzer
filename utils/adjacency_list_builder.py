"""Construct adjacency lists from edge tuples for graph algorithms.

Self loops and duplicate edges are removed by default so downstream passes
receive a clean structure.
"""
import logging
from collections import defaultdict

LOG = logging.getLogger(__name__)


def build_graph(edges, directed=False, keep_self_loops=False):
    """Return an adjacency mapping of neighbours for the given edges."""
    graph = defaultdict(set)
    for source, target in edges or []:
        if source == target and not keep_self_loops:
            continue
        graph[source].add(target)
        if directed:
            graph.setdefault(target, set())
        else:
            graph[target].add(source)
    LOG.debug('built graph with %d nodes', len(graph))
    return {node: sorted(neighbours) for node, neighbours in graph.items()}


def edge_count(edges, directed=False):
    """Return the number of distinct edges after deduplication."""
    graph = build_graph(edges, directed=directed)
    total = sum(len(neighbours) for neighbours in graph.values())
    return total if directed else total // 2


__all__
