"""Redact credentials and secret-looking tokens from text."""
import re

__all__ = ["redact_secrets", "has_secret"]

_MASK = "***REDACTED***"
_PATTERNS = (
    re.compile(r"(?i)\b(api[_-]?key|token|secret|password|passwd|pwd)\b(\s*[:=]\s*)\S+"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._\-]+"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\b[A-Fa-f0-9]{32,}\b"),
)


def redact_secrets(text):
    """Replace secret-looking substrings in *text* with a fixed mask."""
    result = str(text)
    for pattern in _PATTERNS:
        if pattern.groups == 2:
            result = pattern.sub(lambda m: m.group(1) + m.group(2) + _MASK, result)
        else:
            result = pattern.sub(_MASK, result)
    return result


def has_secret(text):
    """Return True when any secret pattern matches *text*."""
    return any(pattern.search(str(text)) for pattern in _PATTERNS)
