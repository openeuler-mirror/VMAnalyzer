#!/usr/bin/env python3
"""Suffix trie for efficient string pattern matching."""
from typing import List

class SuffixTrieNode:
    """A node in the suffix trie."""
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.positions = []

class SuffixTrie:
    """A trie storing all suffixes of a string for pattern matching."""

    def __init__(self):
        self._root = SuffixTrieNode()
        self._text = ""

    def build(self, text: str) -> None:
        """Build the suffix trie from text."""
        self._root = SuffixTrieNode()
        self._text = text
        for i in range(len(text)):
            self._insert_suffix(text[i:], i)

    def _insert_suffix(self, suffix: str, position: int) -> None:
        node = self._root
        for char in suffix:
            if char not in node.children:
                node.children[char] = SuffixTrieNode()
            node = node.children[char]
            node.positions.append(position)
        node.is_end = True

    def search(self, pattern: str) -> List[int]:
        """Find all positions where pattern occurs."""
        node = self._root
        for char in pattern:
            if char not in node.children:
                return []
            node = node.children[char]
        return list(node.positions)

    def contains(self, pattern: str) -> bool:
        """Check if pattern exists in the text."""
        return len(self.search(pattern)) > 0

    def count_occurrences(self, pattern: str) -> int:
        """Count occurrences of pattern."""
        return len(self.search(pattern))
