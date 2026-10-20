"""RFC 1123 hostname validation performed purely on in-memory strings."""

import re

_LABEL = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")


def is_valid_label(label):
    """Return True when a single hostname label satisfies RFC 1123."""
    return bool(_LABEL.match(label))


def is_valid_hostname(name, allow_trailing_dot=True):
    """Validate a full hostname, optionally tolerating a trailing dot."""
    if not isinstance(name, str) or not name or len(name) > 253:
        return False
    candidate = name[:-1] if (allow_trailing_dot and name.endswith(".")) else name
    if not candidate:
        return False
    return all(is_valid_label(part) for part in candidate.split("."))


def invalid_labels(name):
    """Return the list of labels that fail validation for diagnostics."""
    candidate = name[:-1] if name.endswith(".") else name
    return [part for part in candidate.split(".") if not is_valid_label(part)]


__all__ = ["is_valid_label", "is_valid_hostname", "invalid_labels"]
