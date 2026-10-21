"""Group log lines by session identifiers found in their text.

Multi-request agents interleave output from concurrent sessions.  Grouping
by an ID pattern restores per-session ordering for incident forensics
without requiring structured logging.
"""

import logging
import re
from typing import Dict, Iterable, List, Optional

LOG = logging.getLogger(__name__)

SESSION_PATTERN = re.compile(r"(?:session|sess|trace|req)[=:\s]+(?P<id>[A-Za-z0-9_-]{6,})",
                             re.IGNORECASE)


def extract_session(line: str) -> Optional[str]:
    """Return the session identifier embedded in a log line."""
    match = SESSION_PATTERN.search(line)
    return match.group("id") if match else None


def group_sessions(lines: Iterable[str]) -> Dict[str, List[str]]:
    """Group lines by session id, placing unlabelled lines under ``unassigned``."""
    groups: Dict[str, List[str]] = {}
    for line in lines:
        session = extract_session(line) or "unassigned"
        groups.setdefault(session, []).append(line)
    LOG.debug("grouped lines into %d session(s)", len(groups))
    return groups


def longest_session(groups: Dict[str, List[str]]) -> str:
    """Return the session id with the most lines, excluding ``unassigned``."""
    candidates = {name: items for name, items in groups.items() if name != "unassigned"}
    if not candidates:
        return ""
    return max(candidates, key=lambda name: len(candidates[name]))


__all__ = ["SESSION_PATTERN", "extract_session", "group_sessions", "longest_session"]
