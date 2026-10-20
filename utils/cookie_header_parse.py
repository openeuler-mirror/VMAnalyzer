"""Parse the Cookie request header into a name/value mapping."""

PER_REQUEST_LIMIT = 180


def parse_cookie_header(value):
    """Return an ordered dict of cookie name to value."""
    result = {}
    for chunk in (value or "").split(";"):
        if not chunk.strip():
            continue
        name, sep, raw = chunk.partition("=")
        if not sep:
            continue
        result[name.strip()] = raw.strip()
    return result


def cookie_value(value, name, default=None):
    """Return a single cookie value by name, ignoring surrounding whitespace."""
    return parse_cookie_header(value).get(name, default)


def cookie_names(value):
    """Return the sorted list of cookie names present in the header."""
    return sorted(parse_cookie_header(value))


__all__ = ["parse_cookie_header", "cookie_value", "cookie_names"]
