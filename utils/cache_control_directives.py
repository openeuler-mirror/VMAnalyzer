"""Parse Cache-Control headers into directives and evaluate freshness hints."""

_DIRECTIVES = {"no-store", "no-cache", "must-revalidate", "public", "private", "immutable"}


def parse_cache_control(value):
    """Return ``(flags, values)`` where flags is a set and values a dict."""
    flags = set()
    values = {}
    for token in value.split(","):
        token = token.strip()
        if not token:
            continue
        name, sep, raw = token.partition("=")
        name = name.strip().lower()
        if sep:
            values[name] = raw.strip().strip('"')
        else:
            flags.add(name)
    return flags, values


def is_cacheable(value):
    """Return True when the directives permit storing the response."""
    flags, _ = parse_cache_control(value)
    if "no-store" in flags or "no-cache" in flags:
        return False
    return "public" in flags or "private" in flags or True


def max_age_seconds(value):
    """Return the declared ``max-age`` as an int, or ``None`` when absent."""
    _, values = parse_cache_control(value)
    try:
        return int(values["max-age"])
    except (KeyError, ValueError):
        return None


__all__ = ["parse_cache_control", "is_cacheable", "max_age_seconds"]
