"""Coerce JSON scalar values into floats with explicit failure policy.

Metrics exported as JSON sometimes arrive as strings, booleans or nulls.
A lenient coercion with a recorded failure reason keeps aggregation
running while making data quality problems visible.
"""

import logging
from typing import Any, Dict, Optional, Tuple

LOG = logging.getLogger(__name__)


def coerce_number(value: Any) -> Tuple[Optional[float], Optional[str]]:
    """Return ``(number, reason)`` where reason is None on success."""
    if isinstance(value, bool):
        return float(value), None
    if isinstance(value, (int, float)):
        return float(value), None
    if value is None:
        return None, "null"
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None, "empty string"
        try:
            return float(text), None
        except ValueError:
            return None, "not numeric: {!r}".format(value)
    return None, "unsupported type: {}".format(type(value).__name__)


def coerce_record(record: Dict[str, Any]) -> Tuple[Dict[str, float], Dict[str, str]]:
    """Coerce every field, returning values and failure reasons separately."""
    numbers: Dict[str, float] = {}
    failures: Dict[str, str] = {}
    for key, value in record.items():
        number, reason = coerce_number(value)
        if reason is None and number is not None:
            numbers[key] = number
        else:
            failures[key] = reason or "unknown"
    if failures:
        LOG.warning("%d JSON field(s) could not be coerced", len(failures))
    return numbers, failures


__all__ = ["coerce_number", "coerce_record"]
