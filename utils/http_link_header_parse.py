"""Parse HTTP Link headers into target and relation pairs.

Pagination clients rely on ``rel="next"`` links, and hand-splitting the
header on commas breaks when URIs contain quoted commas.  This parser
respects quoting before splitting.
"""

import logging
import re
from typing import Dict, List

LOG = logging.getLogger(__name__)

REL_PATTERN = re.compile(r';\s*rel\s*=\s*"?([^";]+)"?')


def split_links(header: str) -> List[str]:
    """Split a Link header on commas that are outside angle brackets."""
    parts: List[str] = []
    current: List[str] = []
    inside = False
    for char in header:
        if char == "<":
            inside = True
        elif char == ">":
            inside = False
        if char == "," and not inside:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    if current:
        parts.append("".join(current).strip())
    return [part for part in parts if part]


def parse_links(header: str) -> Dict[str, str]:
    """Map relation names to their target URIs."""
    relations: Dict[str, str] = {}
    for part in split_links(header):
        if not part.startswith("<"):
            continue
        closing = part.find(">")
        if closing < 0:
            continue
        target = part[1:closing]
        match = REL_PATTERN.search(part[closing:])
        if match:
            relations[match.group(1).strip()] = target
    LOG.debug("parsed %d link relation(s)", len(relations))
    return relations


def next_link(header: str) -> str:
    """Return the ``next`` relation target, or an empty string."""
    return parse_links(header).get("next", "")


__all__ = ["REL_PATTERN", "split_links", "parse_links", "next_link"]
