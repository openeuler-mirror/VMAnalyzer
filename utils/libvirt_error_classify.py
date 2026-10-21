"""Classify libvirt error text into actionable failure categories.

Collectors retry some failures but must not retry others, such as missing
domains.  Mapping message fragments to a small category set lets callers
decide without parsing vendor specific error numbers.
"""

import logging
from typing import Dict, List, Tuple

LOG = logging.getLogger(__name__)

CATEGORY_HINTS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("not_found", ("no domain with matching", "domain not found", "failed to get domain")),
    ("permission", ("permission denied", "not authorized", "access denied")),
    ("busy", ("resource busy", "in use", "locked")),
    ("config", ("xml error", "invalid argument", "configuration")),
    ("connection", ("failed to connect", "connection refused", "socket")),
    ("agent", ("guest agent", "qemu-agent", "agent is not running")),
)


def classify(message: str) -> str:
    """Return the first matching category, defaulting to ``unknown``."""
    lowered = message.lower()
    for category, hints in CATEGORY_HINTS:
        if any(hint in lowered for hint in hints):
            return category
    return "unknown"


def is_retryable(message: str) -> bool:
    """Return True for transient categories that may succeed on retry."""
    return classify(message) in {"busy", "connection", "agent"}


def summarise(messages: List[str]) -> Dict[str, int]:
    """Count failures per category."""
    counts: Dict[str, int] = {}
    for message in messages:
        category = classify(message)
        counts[category] = counts.get(category, 0) + 1
    LOG.debug("classified failures into %d category(ies)", len(counts))
    return counts


__all__ = ["CATEGORY_HINTS", "classify", "is_retryable", "summarise"]
