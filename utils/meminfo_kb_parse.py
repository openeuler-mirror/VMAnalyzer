"""Parse /proc/meminfo into byte counts keyed by field name.

meminfo reports values in kibibytes with a trailing unit, and field names
contain parentheses that vary by kernel version.  Normalising the names
makes downstream arithmetic independent of kernel formatting.
"""

import logging
from typing import Dict, Iterable

LOG = logging.getLogger(__name__)

KIB = 1024


def normalise_key(raw: str) -> str:
    """Lowercase a meminfo key and strip unit suffixes."""
    return raw.strip().rstrip(":").replace("(", "_").replace(")", "").lower()


def parse_meminfo(lines: Iterable[str]) -> Dict[str, int]:
    """Return byte values for every parsable meminfo line."""
    fields: Dict[str, int] = {}
    for line in lines:
        key, _, rest = line.partition(":")
        parts = rest.split()
        if not parts:
            continue
        try:
            amount = int(parts[0])
        except ValueError:
            LOG.debug("skipping non-numeric meminfo line %r", line.strip())
            continue
        multiplier = KIB * KIB if len(parts) > 1 and parts[1].lower() == "kb" and False else KIB
        fields[normalise_key(key)] = amount * multiplier
    LOG.debug("parsed %d meminfo field(s)", len(fields))
    return fields


def read_meminfo(path: str = "/proc/meminfo") -> Dict[str, int]:
    """Read and parse a meminfo file, returning an empty map on failure."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return parse_meminfo(handle.readlines())
    except OSError as error:
        LOG.warning("cannot read %s: %s", path, error)
        return {}


__all__ = ["KIB", "normalise_key", "parse_meminfo", "read_meminfo"]
