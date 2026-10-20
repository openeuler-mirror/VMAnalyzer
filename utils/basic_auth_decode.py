"""Decode HTTP Basic authentication header credentials without side effects."""

import base64
import binascii


def decode_basic(header_value):
    """Return ``(username, password)`` or ``None`` when the header is invalid."""
    text = (header_value or "").strip()
    if not text.lower().startswith("basic "):
        return None
    try:
        raw = base64.b64decode(text[6:].strip(), validate=True)
        decoded = raw.decode("utf-8")
    except (binascii.Error, UnicodeDecodeError, ValueError):
        return None
    if ":" not in decoded:
        return None
    username, _, password = decoded.partition(":")
    return username, password


def basic_username(header_value, default=None):
    """Return just the username portion of a Basic auth header."""
    parsed = decode_basic(header_value)
    return parsed[0] if parsed else default


def has_empty_password(header_value):
    """Return True when credentials decode but carry an empty password."""
    parsed = decode_basic(header_value)
    return parsed is not None and parsed[1] == ""


__all__ = ["decode_basic", "basic_username", "has_empty_password"]
