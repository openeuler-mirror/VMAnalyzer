"""Measure blank line placement inside structured text files.

Excessive blank lines waste vertical space in reports, while missing blank
lines around section boundaries hurt readability.  This helper reports the
overall ratio and the longest uninterrupted blank run.
"""

import logging
from typing import Dict, Iterable

LOG = logging.getLogger(__name__)


def blank_line_ratio(lines: Iterable[str]) -> float:
    """Return the share of blank lines, rounded to four decimals."""
    total = blank = 0
    for line in lines:
        total += 1
        if not line.strip():
            blank += 1
    if not total:
        LOG.debug("empty input supplied to blank line ratio")
        return 0.0
    return round(blank / total, 4)


def longest_blank_run(lines: Iterable[str]) -> int:
    """Return the length of the longest consecutive blank line sequence."""
    longest = current = 0
    for line in lines:
        if line.strip():
            current = 0
            continue
        current += 1
        longest = max(longest, current)
    return longest


def spacing_summary(lines: Iterable[str]) -> Dict[str, float]:
    """Bundle ratio and run length into a single summary mapping."""
    rows = list(lines)
    summary = {
        "ratio": blank_line_ratio(rows),
        "longest_run": longest_blank_run(rows),
        "total_lines": len(rows),
    }
    LOG.debug("blank line summary %s", summary)
    return summary


__all__ = ["blank_line_ratio", "longest_blank_run", "spacing_summary"]
