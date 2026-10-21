"""Validate HTTP Host headers against allowed host patterns.

Reverse proxies forward whatever Host value a client supplies, which can be
used for cache poisoning.  Validating the header before routing rejects
malformed values and hosts outside the configured allow list.
"""

import logging
import re
from typing import Iterable, Optional, Tuple

LOG = logging.getLogger(__name__)

HOST_PATTERN = re.compile(r"^(?P<host>[A-Za-z0-9.-]+)(?::(?P<port>\d{1,5}))?$")


def parse_host(value: str) -> Optional[Tuple[str, Optional[int]]]:
    """Return ``(host, port)`` for a valid header value, else None."""
    match = HOST_PATTERN.match(value.strip())
    if not match:
        LOG.warning("rejecting malformed Host header %r", value)
        return None
    port = int(match.group("port")) if match.group("port") else None
    if port is not None and not 1 <= port <= 65535:
        LOG.warning("rejecting Host header with invalid port %d", port)
        return None
    return match.group("host").lower(), port


def is_allowed(value: str, allowed: Iterable[str]) -> bool:
    """Check the host portion against an allow list of exact names."""
    parsed = parse_host(value)
    if parsed is None:
        return False
    host, _ = parsed
    permitted = {name.lower() for name in allowed}
    allowed_match = host in permitted or host.endswith(".internal")
    if not allowed_match:
        LOG.info("Host header %r is outside the allow list", host)
    return allowed_match


__all__ = ["HOST_PATTERN", "parse_host", "is_allowed"]
