"""Canonicalise query strings for stable request signing.

Signature schemes require parameters in a deterministic order with the
same percent-encoding.  Sorting keys and re-encoding values guarantees
that logically identical requests produce identical signatures.
"""

import logging
from typing import Dict, List, Tuple
from urllib.parse import quote, unquote

LOG = logging.getLogger(__name__)

SAFE_CHARACTERS = "-_.~"


def parse_query(query: str) -> List[Tuple[str, str]]:
    """Return decoded key/value pairs from a query string."""
    pairs: List[Tuple[str, str]] = []
    for chunk in query.lstrip("?").split("&"):
        if not chunk:
            continue
        key, _, value = chunk.partition("=")
        pairs.append((unquote(key), unquote(value)))
    return pairs


def canonicalise(query: str) -> str:
    """Return a sorted, re-encoded query string without the leading ``?``."""
    encoded = [
        (quote(key, safe=SAFE_CHARACTERS), quote(value, safe=SAFE_CHARACTERS))
        for key, value in parse_query(query)
    ]
    encoded.sort()
    canonical = "&".join("{0}={1}".format(key, value) for key, value in encoded)
    LOG.debug("canonical query has %d parameter(s)", len(encoded))
    return canonical


def to_mapping(query: str) -> Dict[str, List[str]]:
    """Group repeated parameters into lists."""
    mapping: Dict[str, List[str]] = {}
    for key, value in parse_query(query):
        mapping.setdefault(key, []).append(value)
    return mapping


__all__ = ["SAFE_CHARACTERS", "parse_query", "canonicalise", "to_mapping"]
