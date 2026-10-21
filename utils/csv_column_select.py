"""Select and reorder CSV columns by header name.

Exports change column order between releases, which breaks positional
consumers.  Selecting by name keeps downstream parsing stable and reports
missing columns instead of silently shifting values.
"""

import csv
import logging
from typing import Iterable, List, Sequence

LOG = logging.getLogger(__name__)


def parse_header(line: str) -> List[str]:
    """Parse a header line with quote awareness."""
    reader = csv.reader([line])
    for row in reader:
        return [cell.strip() for cell in row]
    return []


def select_columns(rows: Iterable[Sequence[str]], header: List[str],
                   wanted: List[str], fail_fast: bool = False) -> List[List[str]]:
    """Return rows reduced to *wanted* columns in that order."""
    positions = []
    missing = []
    for name in wanted:
        if name in header:
            positions.append(header.index(name))
        else:
            missing.append(name)
            positions.append(-1)
    if missing and fail_fast:
        raise KeyError("missing column(s): {}".format(", ".join(missing)))
    if missing:
        LOG.warning("skipping %d missing column(s): %s", len(missing), ", ".join(missing))
    output: List[List[str]] = []
    for row in rows:
        output.append([row[index] if 0 <= index < len(row) else "" for index in positions])
    return output


def reorder(rows: Iterable[Sequence[str]], header: List[str],
            order: List[str]) -> List[List[str]]:
    """Reorder existing columns without dropping unspecified ones."""
    target = list(order) + [name for name in header if name not in order]
    return select_columns(rows, header, target)


__all__ = ["parse_header", "select_columns", "reorder"]
