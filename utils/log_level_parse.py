"""Parse textual log level names into normalized severities and numbers."""

import logging

_ALIASES = {"warn": "warning", "err": "error", "fatal": "critical",
            "panic": "critical", "trace": "debug", "notice": "info"}


def parse_level(name, default=None):
    """Return a numeric level for a textual name, or ``default``."""
    token = (name or "").strip().lower()
    token = _ALIASES.get(token, token)
    value = logging.getLevelName(token.upper())
    return value if isinstance(value, int) else default


def level_name(value):
    """Return the canonical uppercase name for a numeric level."""
    name = logging.getLevelName(value)
    return name if isinstance(name, str) else str(value)


def is_enabled(message_level, threshold_level):
    """Return True when a message at ``message_level`` passes a threshold."""
    return message_level >= threshold_level


def normalize_level(name, default=logging.INFO):
    """Return an int level, falling back to ``default`` for unknowns."""
    return parse_level(name, default)


__all__ = ["parse_level", "level_name", "is_enabled", "normalize_level"]
