"""Flatten nested configuration dictionaries into dotted key paths."""

SEPARATOR = "."


def flatten_config(data, prefix="", separator=SEPARATOR):
    """Return a flat dict mapping dotted paths to leaf values."""
    flat = {}
    for key, value in (data or {}).items():
        path = "{}{}{}".format(prefix, separator, key) if prefix else str(key)
        if isinstance(value, dict):
            flat.update(flatten_config(value, path, separator))
        else:
            flat[path] = value
    return flat


def unflatten_config(flat, separator=SEPARATOR):
    """Rebuild a nested dict from a previously flattened mapping."""
    nested = {}
    for path, value in (flat or {}).items():
        cursor = nested
        parts = path.split(separator)
        for part in parts[:-1]:
            cursor = cursor.setdefault(part, {})
        cursor[parts[-1]] = value
    return nested


def leaf_paths(data):
    """Return the sorted dotted paths of all non-mapping leaves."""
    return sorted(flatten_config(data))


__all__ = ["flatten_config", "unflatten_config", "leaf_paths"]
