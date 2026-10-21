"""Scan log payloads for common personally identifiable information.

Diagnostic dumps occasionally include guest user names, email addresses or
IP addresses that must not leave the host verbatim.  The scanner reports
categories and counts so redaction can be applied before export.
"""

import logging
import re
from typing import Dict, Iterable

LOG = logging.getLogger(__name__)

PATTERNS = {
    "email": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "uuid": re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
                       r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"),
    "token": re.compile(r"\b(?:ghp|glpat|sk)_[A-Za-z0-9]{16,}\b"),
}


def scan_text(text: str) -> Dict[str, int]:
    """Count PII-like matches per category in a text blob."""
    counts: Dict[str, int] = {}
    for category, pattern in PATTERNS.items():
        found = len(pattern.findall(text))
        if found:
            counts[category] = found
    if counts:
        LOG.warning("PII categories present: %s", ", ".join(sorted(counts)))
    return counts


def scan_lines(lines: Iterable[str]) -> Dict[str, int]:
    """Aggregate PII counts across multiple lines."""
    totals: Dict[str, int] = {}
    for line in lines:
        for category, count in scan_text(line).items():
            totals[category] = totals.get(category, 0) + count
    return totals


def is_clean(lines: Iterable[str]) -> bool:
    """Return True when no PII category was detected."""
    return not scan_lines(lines)


__all__ = ["PATTERNS", "scan_text", "scan_lines", "is_clean"]
