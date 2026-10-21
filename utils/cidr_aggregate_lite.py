"""Aggregate IPv4 CIDR blocks into the smallest covering prefix set.

Firewall rules accumulate overlapping prefixes over time.  Aggregating
them reduces rule count and makes the intended coverage auditable without
requiring a third-party netaddr dependency.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)

Block = Tuple[int, int]


def parse_cidr(text: str) -> Block:
    """Return ``(network, prefix_length)`` for dotted-quad CIDR text."""
    network, _, length = text.strip().partition("/")
    octets = network.split(".")
    if len(octets) != 4:
        raise ValueError("invalid CIDR block: {!r}".format(text))
    value = 0
    for octet in octets:
        number = int(octet)
        if not 0 <= number <= 255:
            raise ValueError("octet out of range in {!r}".format(text))
        value = (value << 8) | number
    prefix = int(length) if length else 32
    if not 0 <= prefix <= 32:
        raise ValueError("prefix length out of range in {!r}".format(text))
    return value, prefix


def contains(parent: Block, child: Block) -> bool:
    """Return True when *parent* fully covers *child*."""
    if parent[1] > child[1]:
        return False
    mask = (0xFFFFFFFF << (32 - parent[1])) & 0xFFFFFFFF if parent[1] else 0
    return (parent[0] & mask) == (child[0] & mask)


def aggregate(blocks: Iterable[Block]) -> List[Block]:
    """Drop blocks already covered by a broader block."""
    ordered = sorted(blocks, key=lambda block: (block[1], block[0]))
    kept: List[Block] = []
    for block in ordered:
        if any(contains(existing, block) for existing in kept):
            continue
        kept.append(block)
    LOG.debug("aggregated %d block(s) into %d", len(list(blocks)), len(kept))
    return kept


__all__ = ["Block", "parse_cidr", "contains", "aggregate"]
