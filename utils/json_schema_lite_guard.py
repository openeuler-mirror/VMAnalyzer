"""Validate JSON-like mappings against a compact field rule table.

Full JSON Schema is overkill for internal payloads, but unchecked fields
cause KeyError deep in reporters.  A small declarative rule set covers the
common cases without adding a dependency.
"""

import logging
from typing import Any, Dict, List, Tuple

LOG = logging.getLogger(__name__)

TYPE_MAP = {"str": str, "int": int, "float": (int, float),
            "bool": bool, "list": list, "dict": dict}


def validate(payload: Dict[str, Any],
             rules: Dict[str, Tuple[str, bool]]) -> List[str]:
    """Validate required and optional fields against declared types."""
    problems: List[str] = []
    for name, (type_name, required) in rules.items():
        if name not in payload:
            if required:
                problems.append("missing required field {!r}".format(name))
            continue
        expected = TYPE_MAP.get(type_name)
        if expected is None:
            problems.append("unknown rule type {!r} for field {!r}".format(type_name, name))
            continue
        if not isinstance(payload[name], expected):
            problems.append("field {!r} should be {}, got {}".format(
                name, type_name, type(payload[name]).__name__))
    if problems:
        LOG.warning("payload validation failed: %s", "; ".join(problems))
    return problems


def require(payload: Dict[str, Any], rules: Dict[str, Tuple[str, bool]]) -> None:
    """Raise ValueError when validation reports any problem."""
    problems = validate(payload, rules)
    if problems:
        raise ValueError("; ".join(problems))


__all__ = ["TYPE_MAP", "validate", "require"]
