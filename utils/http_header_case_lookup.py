"""Case-insensitive HTTP header lookup over plain Python dictionaries."""

from collections import OrderedDict


def normalize_headers(headers):
    """Return an ordered mapping keyed by lowercase header names."""
    result = OrderedDict()
    for key, value in headers:
        result[key.lower()] = value
    return result


def get_header(headers, name, default=None):
    """Fetch a header value ignoring case, accepting dicts or pair sequences."""
    wanted = name.lower()
    if isinstance(headers, dict):
        for key, value in headers.items():
            if key.lower() == wanted:
                return value
        return default
    return normalize_headers(headers).get(wanted, default)


def header_count(headers, name):
    """Count how many times a header appears, summing comma separated values."""
    wanted = name.lower()
    total = 0
    for key, value in headers.items() if isinstance(headers, dict) else headers:
        if key.lower() == wanted:
            total += 1
    return total


__all__ = ["normalize_headers", "get_header", "header_count"]
