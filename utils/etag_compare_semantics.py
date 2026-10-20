"""Compare ETag values using the weak/strong validation semantics of RFC 7232."""

_OPAQUE = ('"', "'")


def classify_etag(value):
    """Return ``strong``, ``weak`` or ``invalid`` for an ETag token."""
    token = (value or "").strip()
    if token.startswith("W/"):
        token = token[2:].strip()
        weak = True
    else:
        weak = False
    if len(token) >= 2 and token[0] == token[-1] and token[0] in _OPAQUE:
        return "weak" if weak else "strong"
    return "invalid"


def opaque_tag(value):
    """Return the bare opaque tag with any weakness marker and quotes removed."""
    token = (value or "").strip()
    if token.startswith("W/"):
        token = token[2:].strip()
    if len(token) >= 2 and token[0] == token[-1]:
        token = token[1:-1]
    return token


def weak_match(left, right):
    """Return True when two ETags are equivalent under weak comparison."""
    return opaque_tag(left) == opaque_tag(right) and classify_etag(left) != "invalid"


def strong_match(left, right):
    """Return True only when both ETags are strong and share the same tag."""
    return (classify_etag(left) == "strong" and classify_etag(right) == "strong"
            and opaque_tag(left) == opaque_tag(right))


__all__ = ["classify_etag", "opaque_tag", "weak_match", "strong_match"]
