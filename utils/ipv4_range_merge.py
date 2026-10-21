"""Merge overlapping IPv4 ranges expressed as integer bounds.

Host inventory exports include overlapping management ranges reported by
different collectors.  Merging them produces a compact, duplicate-free
address plan that can be pushed to firewall tooling.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Range = Tuple[int, int]
OCTET_MASK = 0xFFFFFFFF


def ipv4_to_int(address: str) -> int:
    """Convert dotted-quad notation into a 32-bit integer."""
    parts = address.strip().split(".")
    if len(parts) != 4:
        raise ValueError("invalid IPv4 address: {!r}".format(address))
    value = 0
    for part in parts:
        number = int(part)
        if not 0 <= number <= 255:
            raise ValueError("octet out of range in {!r}".format(address))
        value = (value << 8) | number
    return value


def int_to_ipv4(value: int) -> str:
    """Convert a 32-bit integer back into dotted-quad notation."""
    number = value & OCTET_MASK
    return ".".join(str((number >> shift) & 0xFF) for shift in (24, 16, 8, 0))


def merge_ipv4_ranges(ranges: Iterable[Range]) -> List[Range]:
    """Merge overlapping or adjacent integer address ranges."""
    ordered = sorted((min(start, end), max(start, end)) for start, end in ranges)
    merged: List[Range] = []
    for start, end in ordered:
        if merged and start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            continue
        merged.append((start, end))
    LOG.debug("merged into %d IPv4 range(s)", len(merged))
    return merged


__all__ = ["Range", "ipv4_to_int", "int_to_ipv4", "merge_ipv4_ranges"]
