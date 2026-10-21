"""Parse Linux CPU affinity lists such as ``0-3,6,8-11``.

Affinity masks are exchanged in this compact notation by taskset, virsh and
/proc files.  Expanding them into sorted CPU ids makes validation and set
operations trivial.
"""

import logging
from typing import Iterable, List

LOG = logging.getLogger(__name__)


def parse_affinity(text: str) -> List[int]:
    """Return the sorted CPU ids encoded in an affinity list."""
    cpus = set()
    for chunk in text.replace(" ", "").split(","):
        if not chunk:
            continue
        if "-" in chunk:
            start_text, _, end_text = chunk.partition("-")
            start, end = int(start_text), int(end_text)
            if end < start:
                raise ValueError("reversed CPU range in {!r}".format(chunk))
            cpus.update(range(start, end + 1))
            continue
        cpus.add(int(chunk))
    ordered = sorted(cpus)
    LOG.debug("parsed %d CPU id(s)", len(ordered))
    return ordered


def format_affinity(cpus: Iterable[int]) -> str:
    """Render CPU ids back into compact range notation."""
    values = sorted({int(cpu) for cpu in cpus})
    if not values:
        return ""
    chunks = []
    start = previous = values[0]
    for value in values[1:]:
        if value == previous + 1:
            previous = value
            continue
        chunks.append(str(start) if start == previous else "{}-{}".format(start, previous))
        start = previous = value
    chunks.append(str(start) if start == previous else "{}-{}".format(start, previous))
    return ",".join(chunks)


def overlaps(left: Iterable[int], right: Iterable[int]) -> List[int]:
    """Return the CPU ids shared by two affinity sets."""
    shared = sorted(set(left) & set(right))
    if shared:
        LOG.debug("affinity overlap on %d CPU(s)", len(shared))
    return shared


__all__ = ["parse_affinity", "format_affinity", "overlaps"]
