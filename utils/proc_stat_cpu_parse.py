"""Parse aggregate CPU counters from guest /proc/stat.

The guest agent returns /proc/stat as text, and collectors need the eight
documented counters plus a derived busy percentage.  Handling kernels that
expose fewer fields keeps the parser usable across versions.
"""

import logging
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)

FIELDS = ("user", "nice", "system", "idle", "iowait", "irq", "softirq", "steal")


def parse_cpu_line(line: str) -> Dict[str, int]:
    """Return counters for an aggregate ``cpu`` line, or an empty map."""
    parts = line.split()
    if not parts or parts[0] != "cpu":
        return {}
    counters: Dict[str, int] = {}
    for index, name in enumerate(FIELDS):
        position = index + 1
        if position >= len(parts):
            break
        try:
            counters[name] = int(parts[position])
        except ValueError:
            LOG.warning("non-numeric CPU counter %r", parts[position])
    return counters


def find_cpu_line(lines: Iterable[str]) -> Dict[str, int]:
    """Return the first aggregate CPU counters found in the text."""
    for line in lines:
        counters = parse_cpu_line(line)
        if counters:
            return counters
    LOG.warning("no aggregate cpu line found")
    return {}


def busy_percent(counters: Dict[str, int]) -> float:
    """Return the non-idle share of total CPU time as a percentage."""
    total = sum(counters.values())
    if total <= 0:
        return 0.0
    idle = counters.get("idle", 0) + counters.get("iowait", 0)
    return round((total - idle) / total * 100.0, 2)


def per_cpu(lines: Iterable[str]) -> List[Dict[str, int]]:
    """Return counters for every numbered ``cpuN`` line in order."""
    result: List[Dict[str, int]] = []
    for line in lines:
        parts = line.split()
        if not parts or not parts[0].startswith("cpu") or parts[0] == "cpu":
            continue
        counters = parse_cpu_line("cpu " + " ".join(parts[1:]))
        if counters:
            result.append(counters)
    return result


__all__ = ["FIELDS", "parse_cpu_line", "find_cpu_line", "busy_percent", "per_cpu"]
