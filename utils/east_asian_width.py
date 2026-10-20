"""Measure East-Asian display width of strings for terminal layout."""
import unicodedata

__all__ = ["display_width", "pad_display_width", "truncate_display", "is_wide"]

_WIDE = frozenset("WF")


def is_wide(char):
    """Return True when *char* occupies two terminal columns."""
    return unicodedata.east_asian_width(char) in _WIDE


def display_width(text):
    """Return the number of terminal columns *text* occupies."""
    return sum(2 if is_wide(ch) else (0 if unicodedata.combining(ch) else 1) for ch in str(text))


def truncate_display(text, width, ellipsis="\u2026"):
    """Trim *text* so its display width does not exceed *width*."""
    out, used = [], 0
    for ch in str(text):
        step = 2 if is_wide(ch) else 1
        if used + step > width:
            break
        out.append(ch)
        used += step
    return "".join(out)


def pad_display_width(text, width, fill=" "):
    """Pad *text* with trailing *fill* up to *width* display columns."""
    padding = max(0, width - display_width(text))
    return str(text) + fill[0] * padding
