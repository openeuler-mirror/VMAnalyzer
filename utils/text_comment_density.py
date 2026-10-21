"""Measure the comment density of source-like text.

A very low density suggests undocumented logic, while a density close to
one usually means the file is a license header or commented-out code.
Both signals are useful when triaging unfamiliar modules during a review.
"""

import logging
from typing import Dict, Iterable, Optional, Sequence

LOG = logging.getLogger(__name__)

COMMENT_PREFIXES = ("#", "//", "--", ";", "%")


def comment_density(lines: Iterable[str],
                    prefixes: Optional[Sequence[str]] = None) -> Dict[str, float]:
    """Return code, comment and blank line counts plus their ratio."""
    marks = tuple(prefixes) if prefixes is not None else COMMENT_PREFIXES
    code_lines = blank_lines = comment_lines = 0
    for line in lines:
        stripped = line.strip()
        if not stripped:
            blank_lines += 1
            continue
        code_lines += 1
        if any(stripped.startswith(mark) for mark in marks):
            comment_lines += 1
    total = code_lines + blank_lines
    density = comment_lines / code_lines if code_lines else 0.0
    LOG.debug("comment density %.3f over %d code lines", density, code_lines)
    return {
        "code_lines": code_lines,
        "comment_lines": comment_lines,
        "blank_lines": blank_lines,
        "total_lines": total,
        "density": round(density, 4),
    }


def needs_documentation(stats: Dict[str, float], floor: float = 0.05) -> bool:
    """Report whether a file falls below the minimum comment density."""
    return stats.get("code_lines", 0) >= 20 and stats.get("density", 0.0) < floor


__all__ = ["COMMENT_PREFIXES", "comment_density", "needs_documentation"]
