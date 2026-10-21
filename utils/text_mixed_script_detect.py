"""Detect lines that mix CJK and Latin scripts without separation.

Mixed-script lines usually indicate a partially translated message or a
copy/paste slip in a diagnostic string.  Flagging them helps translators
keep user facing text consistent without blocking the build.
"""

import logging
from typing import Dict, List

LOG = logging.getLogger(__name__)

CJK_RANGES = ((0x4E00, 0x9FFF), (0x3400, 0x4DBF), (0xF900, 0xFAFF))


def _is_cjk(char: str) -> bool:
    """Return True when the character falls inside a CJK ideograph block."""
    code = ord(char)
    return any(low <= code <= high for low, high in CJK_RANGES)


def classify_line(line: str) -> str:
    """Classify a line as ``latin``, ``cjk``, ``mixed`` or ``neutral``."""
    has_cjk = any(_is_cjk(char) for char in line)
    has_latin = any(char.isascii() and char.isalpha() for char in line)
    if has_cjk and has_latin:
        return "mixed"
    if has_cjk:
        return "cjk"
    if has_latin:
        return "latin"
    return "neutral"


def scan_lines(lines: List[str]) -> Dict[str, List[int]]:
    """Group 1-based line numbers by their script classification."""
    buckets: Dict[str, List[int]] = {"latin": [], "cjk": [], "mixed": [], "neutral": []}
    for number, line in enumerate(lines, start=1):
        buckets[classify_line(line)].append(number)
    if buckets["mixed"]:
        LOG.warning("%d line(s) mix CJK and Latin scripts", len(buckets["mixed"]))
    return buckets


__all__ = ["CJK_RANGES", "classify_line", "scan_lines"]
