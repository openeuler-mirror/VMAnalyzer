"""Format host and port pairs for logs and endpoint configuration.

Mixing ``host:port``, ``[ipv6]:port`` and bare IPv6 addresses produces
ambiguous strings that clients cannot parse back.  This helper applies the
bracketed IPv6 convention consistently.
"""

import logging
import ipaddress
from typing import Optional, Tuple

LOG = logging.getLogger(__name__)


def is_ipv6(host: str) -> bool:
    """Return True when *host* is an IPv6 literal."""
    try:
        return isinstance(ipaddress.ip_address(host), ipaddress.IPv6Address)
    except ValueError:
        return False


def format_endpoint(host: str, port: Optional[int] = None) -> str:
    """Return ``host:port`` with IPv6 literals bracketed."""
    literal = host.strip()
    if is_ipv6(literal):
        formatted = "[{}]".format(literal)
    else:
        formatted = literal
    if port is None:
        LOG.debug("formatted endpoint without a port")
        return formatted
    if not 0 < int(port) <= 65535:
        raise ValueError("port must be within 1..65535")
    return "{}:{}".format(formatted, int(port))


def parse_endpoint(value: str) -> Tuple[str, Optional[int]]:
    """Split an endpoint string into host and optional port."""
    text = value.strip()
    if text.startswith("["):
        closing = text.find("]")
        if closing < 0:
            raise ValueError("missing closing bracket in {!r}".format(value))
        host = text[1:closing]
        rest = text[closing + 1:]
        port = int(rest[1:]) if rest.startswith(":") else None
        return host, port
    if text.count(":") == 1:
        host, _, port_text = text.partition(":")
        return host, int(port_text)
    return text, None


__all__ = ["is_ipv6", "format_endpoint", "parse_endpoint"]
