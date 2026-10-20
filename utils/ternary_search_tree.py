"""Ternary search tree storing strings in a compact node chain.

A ternary search tree keeps a character per node plus three ordered children
(less, equal, greater).  It behaves like a trie for lookups while sharing
common prefixes along the equal-child chain, which reduces node count when
keys have long shared stems.
"""

from typing import List, Optional

LOG = __import__("logging").getLogger(__name__)


class _Node:
    __slots__ = ("char", "low", "high", "mid", "terminal")

    def __init__(self, char: str) -> None:
        self.char = char
        self.low: Optional["_Node"] = None
        self.high: Optional["_Node"] = None
        self.mid: Optional["_Node"] = None
        self.terminal = False


class TernarySearchTree:
    """Insert and query strings with lexicographic child ordering."""

    def __init__(self) -> None:
        self._root: Optional[_Node] = None
        self._size = 0

    def insert(self, word: str) -> None:
        """Add *word* to the tree, reusing existing branches."""
        if not word:
            return
        self._root = self._insert(self._root, word, 0)

    def _insert(self, node: Optional[_Node], word: str, pos: int) -> _Node:
        char = word[pos]
        if node is None:
            node = _Node(char)
        if char < node.char:
            node.low = self._insert(node.low, word, pos)
        elif char > node.char:
            node.high = self._insert(node.high, word, pos)
        elif pos + 1 == len(word):
            node.terminal = True
        else:
            node.mid = self._insert(node.mid, word, pos + 1)
        return node

    def __contains__(self, word: str) -> bool:
        """Return True when *word* is present in the tree."""
        node = self._root
        pos = 0
        while node is not None:
            char = word[pos]
            if char < node.char:
                node = node.low
            elif char > node.char:
                node = node.high
            else:
                pos += 1
                if pos == len(word):
                    return node.terminal
                node = node.mid
        return False


def build(words: List[str]) -> TernarySearchTree:
    """Populate a fresh tree from an iterable of words."""
    tree = TernarySearchTree()
    for word in words:
        tree.insert(word)
    return tree


__all__ = ["TernarySearchTree", "build"]
