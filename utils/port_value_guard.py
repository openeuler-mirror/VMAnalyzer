"""Validate individual port values and port lists from configuration.

Ports arrive as strings, ranges or comma separated lists depending on the
source.  Normalising them into ints up front avoids repeated parsing and
catches privileged or out-of-range values early.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)


def parse_port(value, allow_privileged: bool = True) -> int:
    """Return a validated port number or raise ValueError."""
    try:
        port = int(str(value).strip())
    except (TypeError, ValueError):
        raise ValueError("port must be an integer, got {!r}".format(value))
    if not 1 <= port <= 65535:
        raise ValueError("port {} is outside 1..65535".format(port))
    if not allow_privileged and port < 1024:
        LOG.warning("rejecting privileged port %d", port)
        raise ValueError("privileged port {} is not allowed".format(port))
    return port


def parse_list(values: Iterable[str], allow_privileged: bool = True) -> List[int]:
    """Parse a comma separated list of individual ports."""
    ports: List[int] = []
    for chunk in ",".join(values).split(","):
        if chunk.strip():
            ports.append(parse_port(chunk, allow_privileged))
    LOG.debug("parsed %d port(s)", len(ports))
    return sorted(set(ports))


def describe(port: int) -> Tuple[str, bool]:
    """Return the IANA range name and whether the port is privileged."""
    if port < 1024:
        return "system", True
    if port < 49152:
        return "registered", False
    return "dynamic", False


__all__ = ["parse_port", "parse_list", "describe"]
