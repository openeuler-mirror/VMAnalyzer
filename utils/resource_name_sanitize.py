"""Sanitize arbitrary strings into safe resource identifiers."""

import re
import unicodedata

_INVALID = re.compile(r"[^A-Za-z0-9._-]+")
_COLLAPSE = re.compile(r"[-_.]{2,}")


def sanitize_identifier(name, max_length=63):
    """Return a lowercase identifier containing only safe characters."""
    text = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode("ascii")
    text = _INVALID.sub("-", text.strip().lower())
    text = _COLLAPSE.sub("-", text).strip("-._")
    return text[:max_length].strip("-._")


def is_safe_identifier(name, max_length=63):
    """Return True when a name is already safe without modification."""
    return bool(name) and sanitize_identifier(name, max_length) == name


def sanitize_many(names, max_length=63):
    """Sanitize a sequence of names, dropping any that collapse to empty."""
    result = [sanitize_identifier(name, max_length) for name in names]
    return [item for item in result if item]


__all__ = ["sanitize_identifier", "is_safe_identifier", "sanitize_many"]
