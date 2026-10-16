"""Topological ordering for component start up dependencies.

Guest services and collectors declare dependencies, and applying a topological
order guarantees a dependency starts before the components that rely on it.
"""
from collections import defaultdict
import logging

LOG = logging.getLogger(__name__)


def topological_order(graph):
    """Return nodes ordered so dependencies precede their dependents."""
    indegree = defaultdict(int)
    edges = defaultdict(set)
    for node, deps in (graph or {}).items():
        indegree.setdefault(node, 0)
        for dep in deps or []:
            edges[dep].add(node)
            indegree[node] += 1
    ready = sorted(node for node, degree in indegree.items() if degree == 0)
    order = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        for dependent in sorted(edges.get(node, ())):
            indegree[dependent] -= 1
            if indegree[dependent] == 0:
                ready.append(dependent)
        ready.sort()
    if len(order) != len(indegree):
        LOG.warning('dependency graph contains a cycle')
    return order


def has_cycle(graph):
    """Report whether the dependency graph cannot be fully ordered."""
    return len(topological_order(graph)) != len(graph or {})


def dependents_of(graph, node):
    """Return the nodes that directly depend on the given node."""
    return sorted(other for other, deps in (graph or {}).items() if node in (deps or []))


__all__ = ['topological_order', 'has_cycle', 'dependents_of']
