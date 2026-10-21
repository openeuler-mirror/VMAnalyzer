"""Validate hex strings for digit errors and unexpected length.

Corrupted identifiers copied from dashboards typically contain ``O`` or
``l`` characters or an odd digit count.  Guarding before decoding produces
actionable messages instead of obscure tracebacks.
"""

import logging
import re
from typing import List, Optional

LOG = logging.getLogger(__name__)

HEX_PATTERN = re.compile(r"^[0-9a-fA-F]*$")


def problems(value: str, even: bool = True, length: Optional[int] = None) -> List[str]:
    """Return a list of issues with a hex string."""
    issues: List[str] = []
    text = value.strip()
    if not text:
        issues.append("hex string is empty")
        return issues
    if not HEX_PATTERN.match(text):
        invalid = sorted({char for char in text if char not in "0123456789abcdefABCDEF"})
        issues.append("invalid hex character(s): {}".format(", ".join(invalid)))
    if even and len(text) % 2:
        issues.append("hex string has an odd number of digits")
    if length is not None and len(text) != length:
        issues.append("expected {} digits, got {}".format(length, len(text)))
    if issues:
        LOG.warning("hex guard rejected %r", value)
    return issues


def is_valid(value: str, even: bool = True, length: Optional[int] = None) -> bool:
    """Return True when the string has no validation problems."""
    return not problems(value, even, length)


def normalise(value: str) -> Optional[str]:
    """Return a lowercase trimmed hex string, or None when invalid."""
    text = value.strip().lower()
    return text if is_valid(text) else None


__all__ = ["HEX_PATTERN", "problems", "is_valid", "normalise"]
