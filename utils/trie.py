#!/usr/bin/env python3
"""Trie data structure for prefix matching."""
from typing import List, Optional

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self._root = TrieNode()

    def insert(self, word: str) -> None:
        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, s: str) -> Optional[TrieNode]:
        node = self._root
        for ch in s:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def autocomplete(self, prefix: str) -> List[str]:
        node = self._find(prefix)
        results = []
        if node:
            self._collect(node, prefix, results)
        return results

    def _collect(self, node: TrieNode, prefix: str, results: List) -> None:
        if node.is_end:
            results.append(prefix)
        for ch, child in node.children.items():
            self._collect(child, prefix + ch, results)
