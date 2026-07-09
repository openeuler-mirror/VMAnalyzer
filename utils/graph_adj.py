#!/usr/bin/env python3
"""Graph with adjacency list, BFS and DFS traversal."""
from collections import deque
from typing import List, Dict, Set

class Graph:
    def __init__(self):
        self._adj: Dict[str, List[str]] = {}

    def add_edge(self, u: str, v: str) -> None:
        if u not in self._adj:
            self._adj[u] = []
        if v not in self._adj:
            self._adj[v] = []
        self._adj[u].append(v)
        self._adj[v].append(u)

    def bfs(self, start: str) -> List[str]:
        visited, order, queue = set(), [], deque([start])
        visited.add(start)
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self._adj.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return order

    def dfs(self, start: str) -> List[str]:
        visited, order = set(), []
        self._dfs(start, visited, order)
        return order

    def _dfs(self, node: str, visited: Set, order: List) -> None:
        visited.add(node)
        order.append(node)
        for neighbor in self._adj.get(node, []):
            if neighbor not in visited:
                self._dfs(neighbor, visited, order)

    def get_vertices(self) -> List[str]:
        return list(self._adj.keys())
