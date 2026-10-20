"""Check annotation payload sizes against the API server limits."""

MAX_TOTAL_BYTES = 262144
MAX_VALUE_BYTES = 262144
MAX_KEYS = 4096


def value_size(value):
    """Return the UTF-8 encoded byte length of an annotation value."""
    return len(str(value).encode("utf-8"))


def total_size(annotations):
    """Return the combined byte size of all keys and values."""
    return sum(len(str(key).encode("utf-8")) + value_size(value)
               for key, value in (annotations or {}).items())


def size_violations(annotations):
    """Return a list of reasons the annotations exceed documented limits."""
    issues = []
    if len(annotations or {}) > MAX_KEYS:
        issues.append("too many keys")
    if total_size(annotations) > MAX_TOTAL_BYTES:
        issues.append("total size exceeds limit")
    for key, value in (annotations or {}).items():
        if value_size(value) > MAX_VALUE_BYTES:
            issues.append("value too large: {}".format(key))
    return issues


__all__ = ["value_size", "total_size", "size_violations"]
