"""Derive stable short identifiers from arbitrary text.

Dashboards label series with ids that must be unique enough to disambiguate
yet short enough to read.  A truncated SHA-256 keeps collisions negligible
while remaining deterministic across processes and hosts.
"""

import hashlib
import logging
from typing import Iterable, Optional

LOG = logging.getLogger(__name__)


def short_id(text: str, length: int = 10, salt: Optional[str] = None) -> str:
    """Return a deterministic hex identifier for *text*."""
    if length <= 0 or length > 64:
        raise ValueError("length must be within 1..64")
    payload = (salt + "|" + text if salt else text).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()[:length]
    LOG.debug("generated %d character id", len(digest))
    return digest


def series_id(parts: Iterable[str], length: int = 10) -> str:
    """Build an identifier from several label components."""
    return short_id("\x1f".join(parts), length)


def is_lower_hex(value: str) -> bool:
    """Return True when the value looks like a lowercase hex identifier."""
    return bool(value) and all(char in "0123456789abcdef" for char in value)


__all__ = ["short_id", "series_id", "is_lower_hex"]
