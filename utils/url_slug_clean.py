"""Clean URL path fragments into safe slug segments."""
import re

__all__ = ["clean_slug", "slug_join"]

_BAD = re.compile(r"[^a-z0-9\-_]+")
_DASHES = re.compile(r"-{2,}")


def clean_slug(segment):
    """Return a single sanitised, dash-delimited path segment."""
    text = str(segment).strip().lower()
    text = _BAD.sub("-", text)
    text = _DASHES.sub("-", text)
    return text.strip("-_")


def slug_join(segments):
    """Clean and join *segments* into a slash-delimited path."""
    return "/".join(filter(None, (clean_slug(s) for s in segments)))
