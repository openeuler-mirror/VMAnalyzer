"""Compare URLs by scheme and host to detect same-origin mismatches.

Redirect and callback URLs must stay on the expected origin even when the
path differs.  Comparing the origin explicitly is clearer than prefix
matching, which is vulnerable to ``evil-example.com`` lookalikes.
"""

import logging
from typing import Optional, Tuple
from urllib.parse import urlsplit

LOG = logging.getLogger(__name__)


def origin_of(url: str) -> Optional[Tuple[str, str, int]]:
    """Return the lowercase ``(scheme, host, port)`` origin of a URL."""
    try:
        parts = urlsplit(url)
    except ValueError as error:
        LOG.warning("cannot parse URL %r: %s", url, error)
        return None
    if not parts.scheme or not parts.hostname:
        return None
    port = parts.port or (443 if parts.scheme == "https" else 80)
    return parts.scheme.lower(), parts.hostname.lower(), port


def same_origin(left: str, right: str) -> bool:
    """Return True when both URLs share scheme, host and effective port."""
    left_origin, right_origin = origin_of(left), origin_of(right)
    return left_origin is not None and left_origin == right_origin


def ensure_same_origin(url: str, expected: str) -> str:
    """Return the URL unchanged or raise when the origin differs."""
    if not same_origin(url, expected):
        LOG.warning("URL %s does not match the expected origin", url)
        raise ValueError("origin mismatch for {!r}".format(url))
    return url


__all__ = ["origin_of", "same_origin", "ensure_same_origin"]
