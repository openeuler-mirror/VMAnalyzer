"""Parse and order rotated log file indices.

Rotated logs follow ``name.log``, ``name.log.1``, ``name.log.2`` and the
compressed variants.  Sorting those names as plain strings puts ``.10``
before ``.2``, which breaks retention sweeps.
"""

import logging
import re
from typing import Dict, List, Optional, Tuple

LOG = logging.getLogger(__name__)

ROTATE_PATTERN = re.compile(r"^(?P<base>.+?)(?:\.(?P<index>\d+))?(?P<compression>\.(?:gz|xz|bz2|zst))?$")


def parse_rotation(name: str) -> Optional[Tuple[str, int]]:
    """Return ``(base_name, index)`` where the live file has index 0."""
    match = ROTATE_PATTERN.match(name)
    if not match:
        return None
    base = match.group("base")
    compression = match.group("compression") or ""
    if compression:
        base += compression
    index = int(match.group("index") or 0)
    return base, index


def sort_rotations(names: List[str]) -> List[str]:
    """Sort rotated names by base then numeric index ascending."""
    decorated = []
    for name in names:
        parsed = parse_rotation(name)
        decorated.append((parsed[0], parsed[1], name) if parsed else (name, 0, name))
    ordered = [item[2] for item in sorted(decorated)]
    LOG.debug("ordered %d rotated file(s)", len(ordered))
    return ordered


def indices_for(base: str, names: List[str]) -> Dict[str, int]:
    """Map names belonging to *base* to their rotation index."""
    mapping: Dict[str, int] = {}
    for name in names:
        parsed = parse_rotation(name)
        if parsed and parsed[0].startswith(base):
            mapping[name] = parsed[1]
    return mapping


__all__ = ["ROTATE_PATTERN", "parse_rotation", "sort_rotations", "indices_for"]
