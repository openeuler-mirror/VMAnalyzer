#!/usr/bin/env python3
"""Consistent hashing ring for distributed cache and sharding."""
from typing import Dict, List, Optional, Set
from collections import defaultdict
import hashlib

class ConsistentHashRing:
    def __init__(self, virtual_nodes: int = 150):
        self._virtual_nodes = virtual_nodes
        self._ring: Dict[int, str] = {}
        self._sorted_keys: List[int] = []
        self._nodes: Set[str] = set()

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        if node in self._nodes:
            return
        self._nodes.add(node)
        for i in range(self._virtual_nodes):
            vkey = f"{node}#{i}"
            hash_val = self._hash(vkey)
            self._ring[hash_val] = node
        self._sorted_keys = sorted(self._ring.keys())

    def remove_node(self, node: str) -> None:
        if node not in self._nodes:
            return
        self._nodes.discard(node)
        for i in range(self._virtual_nodes):
            vkey = f"{node}#{i}"
            hash_val = self._hash(vkey)
            self._ring.pop(hash_val, None)
        self._sorted_keys = sorted(self._ring.keys())

    def get_node(self, key: str) -> Optional[str]:
        if not self._ring:
            return None
        hash_val = self._hash(key)
        idx = self._binary_search(hash_val)
        return self._ring[self._sorted_keys[idx]]

    def get_nodes(self, key: str, count: int) -> List[str]:
        if not self._ring or count <= 0:
            return []
        hash_val = self._hash(key)
        idx = self._binary_search(hash_val)
        result = []
        seen = set()
        for i in range(len(self._sorted_keys)):
            if len(result) >= count:
                break
            node = self._ring[self._sorted_keys[(idx + i) % len(self._sorted_keys)]]
            if node not in seen:
                seen.add(node)
                result.append(node)
        return result

    def _binary_search(self, hash_val: int) -> int:
        left, right = 0, len(self._sorted_keys) - 1
        while left < right:
            mid = (left + right) // 2
            if self._sorted_keys[mid] < hash_val:
                left = mid + 1
            else:
                right = mid
        return left if left < len(self._sorted_keys) else 0

    @property
    def node_count(self) -> int:
        return len(self._nodes)

    @property
    def ring_size(self) -> int:
        return len(self._ring)

    def get_node_ranges(self) -> Dict[str, int]:
        ranges = defaultdict(int)
        if not self._sorted_keys:
            return ranges
        for i, key in enumerate(self._sorted_keys):
            node = self._ring[key]
            next_key = self._sorted_keys[(i + 1) % len(self._sorted_keys)]
            if next_key > key:
                ranges[node] += next_key - key
            else:
                ranges[node] += (2**128 - key) + next_key
        return ranges

    def list_nodes(self) -> List[str]:
        return sorted(self._nodes)
