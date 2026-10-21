"""Normalise PCI addresses into a canonical zero-padded form.

Inventories mix ``0000:03:00.0`` with ``03:00.0`` and uppercase hex.  A
canonical form lets equality checks and joins work without rewriting every
comparison site.
"""

import logging
import re
from typing import List, Optional

LOG = logging.getLogger(__name__)

SHORT_PATTERN = re.compile(r"^(?:(?P<domain>[0-9a-fA-F]{4}):)?(?P<bus>[0-9a-fA-F]{2}):"
                           r"(?P<slot>[0-9a-fA-F]{2})\.(?P<function>[0-7])$")


def normalize(address: str) -> Optional[str]:
    """Return the canonical ``dddd:bb:ss.f`` lowercase address."""
    match = SHORT_PATTERN.match(address.strip())
    if not match:
        LOG.warning("invalid PCI address %r", address)
        return None
    domain = int(match.group("domain") or "0", 16)
    bus = int(match.group("bus"), 16)
    slot = int(match.group("slot"), 16)
    function = int(match.group("function"), 10)
    canonical = "{:04x}:{:02x}:{:02x}.{}".format(domain, bus, slot, function)
    LOG.debug("normalised PCI address to %s", canonical)
    return canonical


def normalize_all(addresses: List[str]) -> List[str]:
    """Normalise a batch, dropping invalid entries."""
    values = [normalize(address) for address in addresses]
    return [value for value in values if value is not None]


def sort_key(address: str) -> tuple:
    """Return a sortable numeric key for a PCI address."""
    normalised = normalize(address)
    if normalised is None:
        return (1, 0, 0, 0, 0)
    domain, bus, rest = normalised.split(":")
    slot, _, function = rest.partition(".")
    return (0, int(domain, 16), int(bus, 16), int(slot, 16), int(function))


__all__ = ["SHORT_PATTERN", "normalize", "normalize_all", "sort_key"]
