"""Quote TOML scalar values consistently when writing config files.

Hand-rolled config writers often emit bare strings containing ``#`` or
spaces, which TOML parsers reject or misread.  This helper chooses between
basic, literal and multi-line quoting based on the content.
"""

import logging
from typing import Iterable, List, Union

LOG = logging.getLogger(__name__)

Scalar = Union[str, int, float, bool]


def quote_string(value: str) -> str:
    """Return a TOML-safe representation of a string value."""
    if "\n" in value:
        escaped = value.replace('"""', '\\"\\"\\"')
        LOG.debug("using multi-line TOML string of %d characters", len(value))
        return '"""\n{}\n"""'.format(escaped)
    if "'" not in value and "\\" not in value:
        return "'{}'".format(value)
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    escaped = escaped.replace("\t", "\\t").replace("\r", "\\r")
    return '"{}"'.format(escaped)


def render_value(value: Scalar) -> str:
    """Render any supported scalar into TOML syntax."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    return quote_string(str(value))


def render_lines(pairs: Iterable) -> List[str]:
    """Render ``(key, value)`` pairs into ``key = value`` lines."""
    rendered = ["{} = {}".format(key, render_value(value)) for key, value in pairs]
    LOG.debug("rendered %d TOML assignment(s)", len(rendered))
    return rendered


__all__ = ["Scalar", "quote_string", "render_value", "render_lines"]
