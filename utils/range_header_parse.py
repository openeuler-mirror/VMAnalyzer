"""Parse HTTP Range headers of the form ``bytes=start-end`` into spans."""

import re

_TOKEN = re.compile(r"^(\d*)-(\d*)$")


def parse_range_header(value, size=None):
    """Return a list of ``(start, end)`` spans clamped to ``size`` when given."""
    text = (value or "").strip()
    if not text.lower().startswith("bytes="):
        return []
    spans = []
    for part in text[6:].split(","):
        match = _TOKEN.match(part.strip())
        if not match:
            continue
        head, tail = match.group(1), match.group(2)
        if not head and not tail:
            continue
        if head:
            start = int(head)
            end = int(tail) if tail else (size - 1 if size is not None else None)
        else:
            if size is None:
                continue
            length = int(tail)
            start = max(0, size - length)
            end = size - 1
        if end is None:
            continue
        if size is not None:
            end = min(end, size - 1)
        if start <= end:
            spans.append((start, end))
    return spans


def range_is_satisfiable(value, size):
    """Return True when at least one requested span falls inside the entity."""
    return bool(parse_range_header(value, size))


def covered_bytes(value, size):
    """Return the total number of distinct bytes addressed by the header."""
    seen = set()
    for start, end in parse_range_header(value, size):
        seen.update(range(start, end + 1))
    return len(seen)


__all__ = ["parse_range_header", "range_is_satisfiable", "covered_bytes"]
