"""Report trailing whitespace with the exact byte offset of each hit.

Trailing spaces are invisible in diffs and frequently break patch review.
Reporting the offset makes automated cleanup safe because the caller can
rewrite precisely the flagged positions.
"""

import logging
from typing import Dict, Iterable, List, Tuple

LOG = logging.getLogger(__name__)


def trailing_space_report(lines: Iterable[str]) -> Dict[str, object]:
    """Collect line numbers, offsets and widths of trailing whitespace."""
    hits: List[Tuple[int, int, int]] = []
    for number, line in enumerate(lines, start=1):
        stripped = line.rstrip("\r\n")
        body = stripped.rstrip(" \t")
        if len(body) != len(stripped):
            hits.append((number, len(body) + 1, len(stripped) - len(body)))
    report = {
        "lines": len(hits),
        "total_characters": sum(width for _, _, width in hits),
        "positions": hits,
    }
    if hits:
        LOG.debug("trailing whitespace on %d line(s)", len(hits))
    return report


def strip_trailing(lines: Iterable[str]) -> List[str]:
    """Remove trailing blanks but keep the original line endings."""
    cleaned: List[str] = []
    for line in lines:
        ending = ""
        body = line
        for candidate in ("\r\n", "\n", "\r"):
            if body.endswith(candidate):
                ending = candidate
                body = body[: -len(candidate)]
                break
        cleaned.append(body.rstrip(" \t") + ending)
    return cleaned


__all__ = ["trailing_space_report", "strip_trailing"]
