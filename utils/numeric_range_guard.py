"""Validate numeric configuration values against inclusive bounds.

Out-of-range settings such as a zero interval or a negative timeout cause
silent misbehaviour.  Validating once at load time produces a clear message
instead of a stack trace deep inside a collector.
"""

import logging
from typing import Dict, List, Tuple

LOG = logging.getLogger(__name__)


def check(name: str, value, low=None, high=None) -> List[str]:
    """Return a list of validation problems for a single value."""
    problems: List[str] = []
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ["{} must be numeric, got {!r}".format(name, value)]
    if low is not None and number < low:
        problems.append("{} must be >= {}, got {}".format(name, low, number))
    if high is not None and number > high:
        problems.append("{} must be <= {}, got {}".format(name, high, number))
    if problems:
        LOG.warning("range validation failed for %s", name)
    return problems


def validate(specs: Dict[str, Tuple[float, float]], values: Dict[str, object]) -> List[str]:
    """Validate several named values, collecting every problem found."""
    problems: List[str] = []
    for name, (low, high) in specs.items():
        if name not in values:
            problems.append("{} is missing".format(name))
            continue
        problems.extend(check(name, values[name], low, high))
    return problems


def require_valid(specs: Dict[str, Tuple[float, float]], values: Dict[str, object]) -> None:
    """Raise ValueError when any configured value is out of range."""
    problems = validate(specs, values)
    if problems:
        raise ValueError("; ".join(problems))


__all__ = ["check", "validate", "require_valid"]
