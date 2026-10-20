"""Collapse runs of whitespace and bound the number of blank lines."""
import re

__all__ = ["collapse_spaces", "collapse_blank_lines", "normalize_whitespace", "split_nonblank"]

_WS = re.compile(r"[ \t\f\v]+")
_MANY_NEWLINES = re.compile(r"\n{3,}")


def collapse_spaces(text):
    """Replace runs of horizontal whitespace with a single space."""
    return _WS.sub(" ", str(text)).strip()


def collapse_blank_lines(text, keep=1):
    """Limit consecutive newlines so no more than *keep* blank lines remain."""
    return _MANY_NEWLINES.sub("\n" * (keep + 1), str(text))


def normalize_whitespace(text):
    """Apply space collapsing then bound the number of blank lines."""
    return collapse_blank_lines(collapse_spaces(text))


def split_nonblank(text):
    """Return non-blank, space-collapsed lines of *text*."""
    return [collapsed for line in str(text).splitlines() if (collapsed := collapse_spaces(line))]
