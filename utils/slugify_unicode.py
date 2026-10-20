"""Convert arbitrary Unicode text into URL-friendly ASCII slugs."""
import re
import unicodedata

__all__ = ["slugify", "slugify_many"]

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text, sep="-", max_len=80):
    """Return a lowercase, separator-joined slug derived from *text*."""
    decomposed = unicodedata.normalize("NFKD", str(text))
    ascii_only = decomposed.encode("ascii", "ignore").decode("ascii")
    lowered = ascii_only.lower()
    collapsed = _SLUG_RE.sub(sep, lowered).strip(sep)
    return collapsed[:max_len].strip(sep)


def slugify_many(items, sep="-"):
    """Slugify an iterable of strings, dropping any empty results."""
    return [s for s in (slugify(i, sep=sep) for i in items) if s]
