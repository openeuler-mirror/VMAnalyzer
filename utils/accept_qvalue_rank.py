"""Sort Accept-style headers by quality value and specificity."""

_QUALITY_DEFAULT = 1.0


def parse_accept(value):
    """Return a list of ``(item, quality)`` tuples with lowercased items."""
    entries = []
    for token in (value or "").split(","):
        token = token.strip()
        if not token:
            continue
        parts = [part.strip() for part in token.split(";")]
        item = parts[0].lower()
        quality = _QUALITY_DEFAULT
        for param in parts[1:]:
            key, _, raw = param.partition("=")
            if key.strip().lower() == "q":
                try:
                    quality = float(raw.strip())
                except ValueError:
                    quality = 0.0
        entries.append((item, quality))
    return entries


def specificity(item):
    """Score an accept item, where a concrete type beats a wildcard."""
    if item == "*/*":
        return 0
    if item.endswith("/*"):
        return 1
    return 2 + item.count("/")


def rank_accept(value):
    """Return accept items ordered by descending quality then specificity."""
    return [item for item, _ in sorted(parse_accept(value),
                                       key=lambda pair: (pair[1], specificity(pair[0])),
                                       reverse=True)]


def best_accept(value, default="*/*"):
    """Return the highest ranked accept item or ``default`` when empty."""
    ranked = rank_accept(value)
    return ranked[0] if ranked else default


__all__ = ["parse_accept", "specificity", "rank_accept", "best_accept"]
