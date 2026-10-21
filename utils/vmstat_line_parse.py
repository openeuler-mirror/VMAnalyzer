"""Parse /proc/vmstat style counter files into integer mappings.

vmstat exposes kernel memory and scheduler counters as whitespace separated
lines.  Parsing it defensively lets collectors skip malformed rows while
still returning every counter that was readable.
"""

import logging
from typing import Dict, Iterable

LOG = logging.getLogger(__name__)


def parse_vmstat(lines: Iterable[str]) -> Dict[str, int]:
    """Return counter name to integer value for valid rows."""
    counters: Dict[str, int] = {}
    skipped = 0
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            skipped += 1
            continue
        name, raw = parts
        try:
            counters[name] = int(raw)
        except ValueError:
            skipped += 1
    if skipped:
        LOG.warning("skipped %d malformed vmstat row(s)", skipped)
    LOG.debug("parsed %d vmstat counter(s)", len(counters))
    return counters


def counter_delta(before: Dict[str, int], after: Dict[str, int]) -> Dict[str, int]:
    """Return non-negative differences for counters present in both maps."""
    deltas: Dict[str, int] = {}
    for name, value in after.items():
        previous = before.get(name)
        if previous is None:
            continue
        difference = value - previous
        deltas[name] = difference if difference >= 0 else 0
    return deltas


def missing_keys(before: Dict[str, int], after: Dict[str, int]) -> list:
    """Return counters that disappeared between two snapshots."""
    absent = sorted(set(before) - set(after))
    if absent:
        LOG.info("%d counter(s) disappeared between samples", len(absent))
    return absent


__all__ = ["parse_vmstat", "counter_delta", "missing_keys"]
