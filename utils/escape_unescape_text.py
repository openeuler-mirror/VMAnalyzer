"""Escape and unescape control characters in plain text."""
__all__ = ["escape_text", "unescape_text"]

_MAP = {"\\": "\\\\", "\n": "\\n", "\r": "\\r", "\t": "\\t", "\0": "\\0"}
_REVERSE = {v: k for k, v in _MAP.items()}


def escape_text(text):
    """Return *text* with backslashes and control chars escaped."""
    return "".join(_MAP.get(ch, ch) for ch in str(text))


def unescape_text(text):
    """Reverse :func:`escape_text`, decoding the supported escapes."""
    out, i, body = [], 0, str(text)
    while i < len(body):
        pair = body[i:i + 2]
        if pair in _REVERSE:
            out.append(_REVERSE[pair])
            i += 2
        else:
            out.append(body[i])
            i += 1
    return "".join(out)
