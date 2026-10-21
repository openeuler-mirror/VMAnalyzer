"""Report over-long lines in log or configuration dumps.

Terminal and diff tooling degrade badly on very long single lines.  This
helper locates the offenders and summarises the distribution so a caller
can decide whether wrapping or truncation is required.
"""

import logging
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)


def line_length_report(lines: Iterable[str], limit: int = 120) -> Dict[str, object]:
    """Summarise line lengths and list offsets above *limit*."""
    lengths: List[int] = [len(line.rstrip("\n")) for line in lines]
    offenders: List[Tuple[int, int]] = [
        (index + 1, length) for index, length in enumerate(lengths) if length > limit
    ]
    if not lengths:
        LOG.debug("empty input, nothing to measure")
        return {"count": 0, "max_length": 0, "over_limit": 0, "offenders": []}
    report = {
        "count": len(lengths),
        "max_length": max(lengths),
        "mean_length": round(sum(lengths) / len(lengths), 2),
        "over_limit": len(offenders),
        "offenders": offenders,
    }
    LOG.debug("measured %d lines, %d over %d characters", len(lengths), len(offenders), limit)
    return report


def longest_line(lines: Iterable[str]) -> int:
    """Return the 1-based number of the longest line, or zero when empty."""
    best_index = 0
    best_length = -1
    for index, line in enumerate(lines, start=1):
        length = len(line.rstrip("\n"))
        if length > best_length:
            best_index, best_length = index, length
    return best_index


__all__ = ["line_length_report", "longest_line"]
