"""Transpose row-oriented metric records into columns.

Downstream percentiles and vectorised calculations prefer column arrays.
The transpose keeps only keys present in every row by default so the result
stays rectangular and safe to index by position.
"""

import logging
from typing import Dict, Iterable, List, Sequence

LOG = logging.getLogger(__name__)


def transpose(rows: Sequence[Dict[str, float]]) -> Dict[str, List[float]]:
    """Convert rows into a mapping of column name to value list."""
    if not rows:
        return {}
    common = set(rows[0])
    for row in rows[1:]:
        common &= set(row)
    columns: Dict[str, List[float]] = {key: [] for key in sorted(common)}
    for row in rows:
        for key in common:
            columns[key].append(row[key])
    LOG.debug("transposed %d rows into %d column(s)", len(rows), len(columns))
    return columns


def transpose_union(rows: Iterable[Dict[str, float]]) -> Dict[str, List[float]]:
    """Transpose using the union of keys, padding missing values with 0.0."""
    materialised = list(rows)
    if not materialised:
        return {}
    keys = sorted({key for row in materialised for key in row})
    columns: Dict[str, List[float]] = {key: [] for key in keys}
    for row in materialised:
        for key in keys:
            columns[key].append(float(row.get(key, 0.0)))
    return columns


__all__ = ["transpose", "transpose_union"]
