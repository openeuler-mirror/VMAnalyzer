"""Validate enumerated option names against the accepted value set.

CLI options and configuration files occasionally carry near-miss values
such as ``writetrough``.  Validating against the declared set with a
did-you-mean hint turns a silent default into a clear error.
"""

import difflib
import logging
from typing import Iterable, List, Optional, Tuple

LOG = logging.getLogger(__name__)


def validate(value: str, accepted: Iterable[str], ignore_case: bool = True) -> Tuple[Optional[str], Optional[str]]:
    """Return ``(canonical_value, error)`` for an option value."""
    options = list(accepted)
    lookup = {option.lower(): option for option in options} if ignore_case else {
        option: option for option in options
    }
    key = value.strip().lower() if ignore_case else value.strip()
    if key in lookup:
        return lookup[key], None
    matches = difflib.get_close_matches(key, list(lookup), n=1)
    suggestion = lookup[matches[0]] if matches else None
    message = "invalid value {!r}".format(value)
    if suggestion:
        message += ", did you mean {!r}?".format(suggestion)
    LOG.warning(message)
    return None, message


def canonicalise(values: Iterable[str], accepted: Iterable[str]) -> List[str]:
    """Return canonical values, raising on the first invalid entry."""
    options = list(accepted)
    result: List[str] = []
    for value in values:
        canonical, error = validate(value, options)
        if error:
            raise ValueError(error)
        result.append(canonical)
    return result


__all__ = ["validate", "canonicalise"]
