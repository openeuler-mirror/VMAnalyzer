"""Count occurrences of ``key=value`` tokens in collected log lines.

Even without structured logging, agents emit enough ``key=value`` pairs to
build useful distributions.  Counting them reveals dominant error codes,
exit statuses and VM names in a single pass.
"""

import logging
import re
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)

FIELD_PATTERN = re.compile(r"(?P<key>[A-Za-z_][\w.-]*)=(?P<value>[^\s,;\"']+)")


def extract_fields(line: str) -> Dict[str, str]:
    """Return the last ``key=value`` assignment per key in a line."""
    return {match.group("key"): match.group("value")
            for match in FIELD_PATTERN.finditer(line)}


def count_values(lines: Iterable[str], key: str) -> Dict[str, int]:
    """Count how often each value of *key* appears across lines."""
    counts: Dict[str, int] = {}
    for line in lines:
        value = extract_fields(line).get(key)
        if value is not None:
            counts[value] = counts.get(value, 0) + 1
    LOG.debug("counted %d distinct value(s) for key %s", len(counts), key)
    return counts


def top_values(lines: Iterable[str], key: str, limit: int = 5) -> List[Tuple[str, int]]:
    """Return the most frequent values for a key."""
    counts = count_values(lines, key)
    return sorted(counts.items(), key=lambda item: item[1], reverse=True)[:limit]


__all__ = ["FIELD_PATTERN", "extract_fields", "count_values", "top_values"]
