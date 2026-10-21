"""Map free-form severity names onto a canonical ordered scale.

Different exporters use ``WARN``, ``warn``, ``p2`` or ``major`` for the same
concept.  A single mapping avoids brittle comparisons and keeps routing
rules readable.
"""

import logging
from typing import Dict, Iterable, Optional

LOG = logging.getLogger(__name__)

ALIASES: Dict[str, str] = {
    "info": "info", "notice": "info", "p4": "info", "low": "info",
    "warning": "warning", "warn": "warning", "p3": "warning", "minor": "warning",
    "error": "error", "err": "error", "p2": "error", "major": "error",
    "critical": "critical", "crit": "critical", "fatal": "critical",
    "p1": "critical", "emergency": "critical",
}
ORDER = ("info", "warning", "error", "critical")


def normalise(name: str) -> Optional[str]:
    """Return the canonical severity or None for an unknown name."""
    canonical = ALIASES.get(str(name).strip().lower())
    if canonical is None:
        LOG.warning("unknown severity name %r", name)
    return canonical


def rank(name: str) -> int:
    """Return the ordinal of the canonical severity, -1 when unknown."""
    canonical = normalise(name)
    return ORDER.index(canonical) if canonical in ORDER else -1


def highest(names: Iterable[str]) -> Optional[str]:
    """Return the most severe canonical name in a collection."""
    ranks = [(rank(name), normalise(name)) for name in names]
    valid = [(value, label) for value, label in ranks if label is not None]
    if not valid:
        return None
    return max(valid)[1]


__all__ = ["ALIASES", "ORDER", "normalise", "rank", "highest"]
