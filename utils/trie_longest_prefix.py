"""Find the longest stored prefix of a string in a character trie.

Routing rules and metric name hierarchies both need longest-prefix matching
rather than first-match lookup.  A trie keeps lookup linear in the input
length regardless of how many prefixes are registered.
"""

import logging
from typing import Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)


class PrefixTrie:
    """Map string prefixes to values and query the longest match."""

    def __init__(self) -> None:
        self._children: List[Dict[str, int]] = [{}]
        self._values: List[Optional[object]] = [None]

    def insert(self, prefix: str, value: object) -> None:
        """Register *value* for *prefix*, replacing an earlier value."""
        node = 0
        for char in prefix:
            table = self._children[node]
            if char not in table:
                table[char] = len(self._children)
                self._children.append({})
                self._values.append(None)
            node = table[char]
        self._values[node] = value

    def longest_prefix(self, text: str) -> Tuple[str, Optional[object]]:
        """Return the longest matching prefix and its value."""
        node = 0
        best: Tuple[str, Optional[object]] = ("", None)
        consumed = []
        for char in text:
            table = self._children[node]
            if char not in table:
                break
            node = table[char]
            consumed.append(char)
            if self._values[node] is not None:
                best = ("".join(consumed), self._values[node])
        LOG.debug("longest prefix for %r is %r", text, best[0])
        return best

    def __len__(self) -> int:
        """Return the number of registered prefixes."""
        return sum(1 for value in self._values if value is not None)


__all__ = ["PrefixTrie"]
