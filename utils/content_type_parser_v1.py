"""Parse Content-Type header values into media type plus structured parameters."""

import re

_PARAM = re.compile(r';\s*([A-Za-z0-9!#$&^_.+-]+)\s*=\s*(?:"([^"]*)"|([^;]*))')


def parse_content_type(value):
    """Return ``(media_type, params)`` with a lowercased media type."""
    main, _, rest = value.partition(";")
    media = main.strip().lower()
    params = {}
    for match in _PARAM.finditer(";" + rest):
        key = match.group(1).lower()
        params[key] = (match.group(2) if match.group(2) is not None else match.group(3)).strip()
    return media, params


def charset_of(value, default="utf-8"):
    """Return the declared charset parameter, lowercased, or ``default``."""
    _, params = parse_content_type(value)
    return params.get("charset", default).lower()


def is_json_media(value):
    """Return True when the media type is JSON (including ``+json`` suffixes)."""
    media, _ = parse_content_type(value)
    return media == "application/json" or media.endswith("+json")


__all__ = ["parse_content_type", "charset_of", "is_json_media"]
