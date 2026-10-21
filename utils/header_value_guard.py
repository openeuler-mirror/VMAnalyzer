"""Sanitise HTTP header values before forwarding them upstream.

Header values must not contain control characters or be unreasonably long,
otherwise proxies reject or mangle the request.  Guarding at the boundary
prevents corrupted telemetry payloads.
"""

import logging
from typing import Dict, Optional, Tuple

LOG = logging.getLogger(__name__)

MAX_LENGTH = 8192
FORBIDDEN = set("\r\n\x00")


def check(name: str, value: str) -> Optional[str]:
    """Return a problem description for a header value, or None."""
    if value is None:
        return "header {!r} has no value".format(name)
    text = str(value)
    if any(char in FORBIDDEN for char in text):
        return "header {!r} contains a control character".format(name)
    if len(text) > MAX_LENGTH:
        return "header {!r} exceeds {} characters".format(name, MAX_LENGTH)
    if text != text.strip():
        return "header {!r} has surrounding whitespace".format(name)
    return None


def sanitise(headers: Dict[str, str]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """Return accepted headers and rejected names with reasons."""
    accepted: Dict[str, str] = {}
    rejected: Dict[str, str] = {}
    for name, value in headers.items():
        reason = check(name, value)
        if reason:
            rejected[name] = reason
            continue
        accepted[name] = str(value)
    if rejected:
        LOG.warning("rejected %d unsafe header(s)", len(rejected))
    return accepted, rejected


def require_valid(headers: Dict[str, str]) -> None:
    """Raise ValueError listing every unsafe header."""
    _, rejected = sanitise(headers)
    if rejected:
        raise ValueError("; ".join(sorted(rejected.values())))


__all__ = ["MAX_LENGTH", "check", "sanitise", "require_valid"]
