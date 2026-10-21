"""Parse the whitespace-aligned table printed by ``virsh list``.

The table uses fixed-width columns whose boundaries shift with the longest
domain name.  Splitting on two or more spaces recovers the intended fields
without depending on exact column offsets.
"""

import logging
import re
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)

COLUMN_SPLIT = re.compile(r"\s{2,}")
HEADER_PREFIXES = ("Id", "Name", "State")


def parse_list_rows(text: str) -> List[Dict[str, str]]:
    """Return one record per domain row of virsh list output."""
    rows: List[Dict[str, str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("-") or stripped.startswith("Id"):
            continue
        columns = COLUMN_SPLIT.split(stripped)
        if len(columns) < 3:
            continue
        identifier, name, state = columns[0], columns[1], " ".join(columns[2:])
        if not identifier.replace("-", "").isdigit():
            continue
        rows.append({"id": identifier, "name": name, "state": state})
    LOG.debug("parsed %d domain row(s)", len(rows))
    return rows


def running_domains(rows: Iterable[Dict[str, str]]) -> List[str]:
    """Return names of domains whose state is running or blocked."""
    return [row["name"] for row in rows if row["state"].split()[0] in ("running", "blocked")]


def find_domain(rows: Iterable[Dict[str, str]], name: str) -> Dict[str, str]:
    """Return the record for a domain name, or an empty mapping."""
    for row in rows:
        if row["name"] == name:
            return row
    return {}


__all__ = ["COLUMN_SPLIT", "parse_list_rows", "running_domains", "find_domain"]
