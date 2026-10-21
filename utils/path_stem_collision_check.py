"""Detect files whose stems collide after normalisation.

Uploaded artefacts from different hosts often normalise to the same stem
once dots, spaces and case are folded.  Catching collisions before writing
prevents silent overwrites in shared report directories.
"""

import logging
import re
from typing import Dict, List

LOG = logging.getLogger(__name__)

NORMALISE_PATTERN = re.compile(r"[^0-9a-zA-Z]+")


def normalise_stem(name: str) -> str:
    """Fold a file name into a lowercase alphanumeric stem."""
    base = name.rsplit("/", 1)[-1]
    stem = base.rsplit(".", 1)[0] if "." in base else base
    return NORMALISE_PATTERN.sub("_", stem).strip("_").lower()


def collision_groups(names: List[str]) -> Dict[str, List[str]]:
    """Map each normalised stem to the original names that share it."""
    groups: Dict[str, List[str]] = {}
    for name in names:
        groups.setdefault(normalise_stem(name), []).append(name)
    collisions = {stem: items for stem, items in groups.items() if len(items) > 1}
    if collisions:
        LOG.warning("detected %d stem collision group(s)", len(collisions))
    return collisions


def is_safe(names: List[str]) -> bool:
    """Return True when no stem collisions exist in the supplied names."""
    return not collision_groups(names)


__all__ = ["NORMALISE_PATTERN", "normalise_stem", "collision_groups", "is_safe"]
