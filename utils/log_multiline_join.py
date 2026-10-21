"""Rejoin stack trace continuation lines into single logical records.

Journalctl and file-based logs split exceptions across many indented lines.
Parsers that treat every line as a record lose the trace.  This helper
attaches continuation lines to the record that started them.
"""

import logging
from typing import Iterable, List, Optional

LOG = logging.getLogger(__name__)

CONTINUATION_PREFIXES = (" ", "\t", "at ", "Traceback", "Caused by", "... ")


def is_continuation(line: str) -> bool:
    """Return True when the line continues the previous record."""
    stripped = line.rstrip("\n")
    return bool(stripped) and (stripped[0].isspace() or
                               stripped.startswith(CONTINUATION_PREFIXES[2:]))


def join_records(lines: Iterable[str], header_pattern: Optional[str] = None) -> List[str]:
    """Merge continuation lines into their originating record."""
    records: List[str] = []
    for line in lines:
        text = line.rstrip("\n")
        if not text:
            continue
        if not records or (not is_continuation(line) and
                           (header_pattern is None or text.startswith(header_pattern))):
            records.append(text)
            continue
        records[-1] = records[-1] + "\n" + text
    LOG.debug("joined log lines into %d record(s)", len(records))
    return records


def trace_depth(record: str) -> int:
    """Return the number of continuation lines in a joined record."""
    return max(0, record.count("\n"))


__all__ = ["CONTINUATION_PREFIXES", "is_continuation", "join_records", "trace_depth"]
