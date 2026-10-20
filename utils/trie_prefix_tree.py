"""Prefix trie supporting insertion, exact lookup and prefix enumeration.

The trie stores strings as character paths from a virtual root node.  It is
useful for autocomplete style workloads where the set of candidate keys is
known up front and repeated prefix walks are cheap.
"""

import logging
from typing import Dict, Iterator, List, Optional

LOG = logging.getLogger(__name__)


class PrefixTrie:
    """Character trie with a terminal marker per stored key."""

    def __init__(self) -> None:
        self._children: List[Dict[str, int]] = [{}]
        self._terminal: List[bool] = [False]

    def insert(self, word: str) -> None:
        """Insert *word* into the trie, creating nodes along the way."""
        node = 0
        for ch in word:
            nxt = self._children[node].get(ch)
            if nxt is None:
                nxt = len(self._children)
                self._children[node][ch] = nxt
                self._children.append({})
                self._terminal.append(False)
            node = nxt
        self._terminal[node] = True

    def contains(self, word: str) -> bool:
        """Return True when *word* was previously inserted."""
        node = self._find(word)
        return node is not None and self._terminal[node]

    def _find(self, prefix: str) -> Optional[int]:
        node = 0
        for ch in prefix:
            node = self._children[node].get(ch, -1)
            if node < 0:
                return None
        return node

    def completions(self, prefix: str) -> Iterator[str]:
        """Yield every stored key that starts with *prefix*."""
        node = self._find(prefix)
        if node is None:
            return
        stack = [(node, prefix)]
        while stack:
            current, text = stack.pop()
            if self._terminal[current]:
                yield text
            for ch, child in self._children[current].items():
                stack.append((child, text + ch))


def build_from_words(words: List[str]) -> PrefixTrie:
    """Convenience helper returning a trie populated with *words*."""
    trie = PrefixTrie()
    for word in words:
        trie.insert(word)
    return trie


__all__ = ["PrefixTrie", "build_from_words"]
