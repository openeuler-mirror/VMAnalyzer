"""Sort records by a tuple of nullable priority fields.

Nullable priority fields break plain tuple sorting in Python 3 because
comparisons between None and strings raise.  Wrapping each component with a
sentinel keeps missing values last without special casing every column.
"""

import logging
from typing import Any, Iterable, List, Tuple

LOG = logging.getLogger(__name__)

MISSING_RANK = (1, "")


def _rank(value: Any) -> Tuple[int, Any]:
    """Wrap a value so that None always sorts after real values."""
    return MISSING_RANK if value is None else (0, value)


def sort_by_priority(records: Iterable[dict], fields: List[str],
                     reverse: bool = False) -> List[dict]:
    """Sort mappings by nullable fields, pushing None values last."""
    def key(record: dict) -> Tuple:
        return tuple(_rank(record.get(field)) for field in fields)

    ordered = sorted(records, key=key, reverse=reverse)
    LOG.debug("sorted %d record(s) by %d field(s)", len(ordered), len(fields))
    return ordered


def first_by_priority(records: Iterable[dict], field: str,
                      default: Any = None) -> Any:
    """Return the value of *field* from the highest priority record."""
    ordered = sort_by_priority(records, [field])
    if not ordered:
        return default
    return ordered[0].get(field, default)


__all__ = ["MISSING_RANK", "sort_by_priority", "first_by_priority"]
