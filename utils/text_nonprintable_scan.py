"""Locate non-printable characters in captured guest output.

Guest commands occasionally return terminal control sequences that break
JSON serialisation or make dashboards unreadable.  Scanning for such bytes
before storing the payload keeps downstream consumers stable.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)


def _is_printable(char: str) -> bool:
    """Return True for characters safe to emit into plain text output."""
    return char.isprintable() or char in ("\n", "\r", "\t")


def scan_nonprintable(text: str) -> List[Tuple[int, int, str]]:
    """Return (line, column, escaped-char) tuples for non-printable chars."""
    findings: List[Tuple[int, int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for column, char in enumerate(line, start=1):
            if not _is_printable(char):
                findings.append((line_no, column, repr(char)))
    if findings:
        LOG.warning("found %d non-printable character(s)", len(findings))
    return findings


def contains_nonprintable(text: str) -> bool:
    """Fast predicate used to skip payloads that need no cleaning."""
    return any(not _is_printable(char) for char in text)


def summarize(findings: Iterable[Tuple[int, int, str]]) -> str:
    """Render findings as a compact single-line summary."""
    rows = list(findings)
    if not rows:
        return "clean"
    return "{} issue(s), first at line {} column {}".format(len(rows), rows[0][0], rows[0][1])


__all__ = ["scan_nonprintable", "contains_nonprintable", "summarize"]
