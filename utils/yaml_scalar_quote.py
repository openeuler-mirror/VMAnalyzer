"""Quote YAML scalars that would otherwise be parsed as other types.

Values such as ``on``, ``no``, ``1.0`` or ``*ref`` change meaning when a
YAML parser reads them unquoted.  Detecting those ambiguous cases before
emission keeps generated manifests faithful to the source data.
"""

import logging
import re
from typing import Iterable, List

LOG = logging.getLogger(__name__)

AMBIGUOUS_WORDS = {"yes", "no", "true", "false", "on", "off", "null", "~"}
NUMERIC_PATTERN = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$")


def needs_quotes(text: str) -> bool:
    """Return True when the scalar is ambiguous without quotes."""
    if not text:
        return True
    if text.lower() in AMBIGUOUS_WORDS or NUMERIC_PATTERN.match(text):
        return True
    return text[0] in "-?:,[]{}#&*!|>'\"%@`" or text != text.strip()


def quote_scalar(text: str) -> str:
    """Return the value, quoted with single quotes only when required."""
    if not needs_quotes(text):
        return text
    escaped = text.replace("'", "''")
    LOG.debug("quoted ambiguous YAML scalar %r", text)
    return "'{}'".format(escaped)


def quote_lines(values: Iterable[str]) -> List[str]:
    """Quote a batch of scalars for list rendering."""
    return [quote_scalar(value) for value in values]


__all__ = ["AMBIGUOUS_WORDS", "needs_quotes", "quote_scalar", "quote_lines"]
