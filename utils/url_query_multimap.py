"""Parse a URL query string into an ordered multimap without touching the network."""

from urllib.parse import parse_qsl, urlencode

MAX_PAIRS = 256


def query_pairs(query):
    """Return a list of decoded ``(key, value)`` pairs from a query string."""
    stripped = query[1:] if query.startswith("?") else query
    return parse_qsl(stripped, keep_blank_values=True)[:MAX_PAIRS]


def query_multimap(query):
    """Return a dict mapping each key to the list of values it carries."""
    result = {}
    for key, value in query_pairs(query):
        result.setdefault(key, []).append(value)
    return result


def query_lookup(query, key, default=None):
    """Return the first value associated with ``key`` or ``default``."""
    for item_key, item_value in query_pairs(query):
        if item_key == key:
            return item_value
    return default


def query_roundtrip(query):
    """Re-encode the parsed pairs, useful for canonical comparison checks."""
    return urlencode(query_pairs(query), doseq=True)


__all__ = ["query_pairs", "query_multimap", "query_lookup", "query_roundtrip"]
