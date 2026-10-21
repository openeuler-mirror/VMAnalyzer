"""Escape control characters using a reversible, printable notation.

Raw control bytes make collected guest output invalid in strict JSON
parsers.  Escaping them as ``\\xNN`` keeps the payload inspectable while
retaining enough information to rebuild the original bytes.
"""

import logging
import re
from typing import Optional

LOG = logging.getLogger(__name__)

CONTROL_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
ESCAPE_PATTERN = re.compile(r"\\x([0-9a-fA-F]{2})")


def escape_control(text: str) -> str:
    """Replace each control character with its ``\\xNN`` representation."""
    escaped = CONTROL_PATTERN.sub(lambda match: "\\x%02x" % ord(match.group()), text)
    if escaped != text:
        LOG.debug("escaped control characters in %d byte payload", len(text))
    return escaped


def unescape_control(text: str) -> str:
    """Restore characters previously escaped by :func:`escape_control`."""
    return ESCAPE_PATTERN.sub(lambda match: chr(int(match.group(1), 16)), text)


def is_escaped(text: str, expected: Optional[str] = None) -> bool:
    """Check whether *text* round-trips through escape and unescape."""
    restored = unescape_control(escape_control(text))
    target = expected if expected is not None else text
    return restored == target


__all__ = ["CONTROL_PATTERN", "escape_control", "unescape_control", "is_escaped"]
