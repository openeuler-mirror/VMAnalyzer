"""Normalise MAC addresses and extract their vendor OUI prefix.

Inventory reports include MACs in colon, dash and bare hex notation.  A
single normaliser plus OUI extraction lets asset grouping work without an
external IEEE database dump.
"""

import logging
import re
from typing import Iterable, Optional

LOG = logging.getLogger(__name__)

NON_HEX_PATTERN = re.compile(r"[^0-9a-fA-F]")


def normalise_mac(value: str, separator: str = ":") -> Optional[str]:
    """Return a lowercase MAC with the requested separator, or None."""
    cleaned = NON_HEX_PATTERN.sub("", value)
    if len(cleaned) != 12:
        LOG.warning("invalid MAC address length for %r", value)
        return None
    lowered = cleaned.lower()
    return separator.join(lowered[index:index + 2] for index in range(0, 12, 2))


def oui_of(value: str) -> Optional[str]:
    """Return the first three octets as an uppercase OUI string."""
    normalised = normalise_mac(value, separator="")
    if normalised is None:
        return None
    return normalised[:6].upper()


def group_by_oui(values: Iterable[str]) -> dict:
    """Group MAC addresses by their OUI prefix."""
    groups = {}
    for value in values:
        prefix = oui_of(value)
        if prefix:
            groups.setdefault(prefix, []).append(value)
    LOG.debug("grouped addresses into %d OUI bucket(s)", len(groups))
    return groups


__all__ = ["normalise_mac", "oui_of", "group_by_oui"]
