"""Find repeated lines that are likely copy/paste leftovers.

Duplicated configuration stanzas or repeated log headers can double the
cost of parsing while hiding the real content.  The report keeps the first
occurrence and every later position so the caller can trim selectively.
"""

import logging
from collections import OrderedDict
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)


def duplicate_lines(lines: Iterable[str], ignore_case: bool = False,
                    min_length: int = 1) -> Dict[str, List[int]]:
    """Map each duplicated line to the 1-based numbers where it appears."""
    seen: "OrderedDict[str, List[int]]" = OrderedDict()
    for number, raw in enumerate(lines, start=1):
        text = raw.strip()
        if len(text) < min_length:
            continue
        key = text.lower() if ignore_case else text
        seen.setdefault(key, []).append(number)
    duplicates = {key: numbers for key, numbers in seen.items() if len(numbers) > 1}
    if duplicates:
        LOG.debug("found %d duplicated line pattern(s)", len(duplicates))
    return duplicates


def duplicate_ratio(lines: Iterable[str], ignore_case: bool = False) -> float:
    """Return the fraction of lines that repeat an earlier line."""
    rows = [line.strip() for line in lines if line.strip()]
    if not rows:
        return 0.0
    unique = {row.lower() if ignore_case else row for row in rows}
    return round(1.0 - len(unique) / len(rows), 4)


__all__ = ["duplicate_lines", "duplicate_ratio"]
