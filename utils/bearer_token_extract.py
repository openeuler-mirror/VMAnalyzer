"""Extract and sanity check Bearer tokens from Authorization headers."""

import re

_SCHEME = re.compile(r"^bearer\s+(.+)$", re.IGNORECASE)
_TOKEN_CHARS = re.compile(r"^[A-Za-z0-9\-._~+/]+=*$")


def extract_bearer(header_value):
    """Return the bearer token text, or ``None`` when the scheme is absent."""
    match = _SCHEME.match((header_value or "").strip())
    return match.group(1).strip() if match else None


def is_plausible_token(token):
    """Return True when the token uses the permissive RFC 6750 character set."""
    return bool(token) and bool(_TOKEN_CHARS.match(token))


def bearer_summary(header_value):
    """Return a short non-sensitive description of the credential."""
    token = extract_bearer(header_value)
    if token is None:
        return {"scheme": "unknown", "length": 0}
    return {"scheme": "bearer", "length": len(token), "plausible": is_plausible_token(token)}


__all__ = ["extract_bearer", "is_plausible_token", "bearer_summary"]
