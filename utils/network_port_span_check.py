"""Detect overlapping port spans in service definitions.

Port allocation files list ranges such as ``8000-8100``.  Overlaps cause
two services to bind the same socket, which fails only at runtime.  The
checker reports conflicts before deployment.
"""

import logging
from typing import List, Tuple

LOG = logging.getLogger(__name__)

Span = Tuple[int, int]


def parse_span(text: str) -> Span:
    """Parse ``start-end`` or a single port into an inclusive span."""
    cleaned = text.strip()
    if "-" in cleaned:
        start_text, _, end_text = cleaned.partition("-")
        start, end = int(start_text), int(end_text)
    else:
        start = end = int(cleaned)
    if not (1 <= start <= 65535 and 1 <= end <= 65535):
        raise ValueError("port span out of range: {!r}".format(text))
    if end < start:
        start, end = end, start
    return start, end


def find_conflicts(spans: List[Span]) -> List[Tuple[int, int, int, int]]:
    """Return pairs of overlapping inclusive spans."""
    ordered = sorted(spans)
    conflicts = []
    for index, (start, end) in enumerate(ordered):
        for other_start, other_end in ordered[index + 1:]:
            if other_start > end:
                break
            if other_start <= end and other_end >= start:
                conflicts.append((start, end, other_start, other_end))
    if conflicts:
        LOG.warning("detected %d overlapping port span(s)", len(conflicts))
    return conflicts


def total_ports(spans: List[Span]) -> int:
    """Return the number of unique ports covered by the spans."""
    covered = set()
    for start, end in spans:
        covered.update(range(start, end + 1))
    return len(covered)


__all__ = ["Span", "parse_span", "find_conflicts", "total_ports"]
