"""Safely read nested values from configuration dicts using dotted paths."""

_MISSING = object()


def get_path(data, path, default=None, separator="."):
    """Return the value at a dotted path, descending through mappings."""
    cursor = data
    for part in str(path).split(separator):
        if isinstance(cursor, dict) and part in cursor:
            cursor = cursor[part]
        else:
            return default
    return cursor


def has_path(data, path, separator="."):
    """Return True when the dotted path resolves to a value."""
    return get_path(data, path, _MISSING, separator) is not _MISSING


def require_paths(data, paths, separator="."):
    """Return the list of dotted paths that are absent from ``data``."""
    return [path for path in paths if not has_path(data, path, separator)]


def get_int(data, path, default=0, separator="."):
    """Return an integer value at ``path``, coercing strings when possible."""
    value = get_path(data, path, None, separator)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


__all__ = ["get_path", "has_path", "require_paths", "get_int"]
