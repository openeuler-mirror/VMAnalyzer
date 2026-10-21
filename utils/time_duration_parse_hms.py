"""Parse compact duration strings such as ``1h30m`` or ``90s``.

Command line options and configuration files use terse duration literals,
but Python has no built-in parser.  This helper accepts the common suffix
set and rejects ambiguous or negative input.
"""

import logging
import re

LOG = logging.getLogger(__name__)

DURATION_PATTERN = re.compile(r"^(?:(?P<days>\d+)d)?(?:(?P<hours>\d+)h)?"
                              r"(?:(?P<minutes>\d+)m)?(?:(?P<seconds>\d+)s)?$")
UNIT_SECONDS = {"d": 86400, "h": 3600, "m": 60, "s": 1}


def parse_duration(text: str) -> float:
    """Return the total seconds encoded in *text*."""
    value = text.strip().lower()
    if not value:
        raise ValueError("empty duration string")
    if value.isdigit():
        return float(value)
    match = DURATION_PATTERN.match(value)
    if not match or not any(match.groupdict().values()):
        raise ValueError("unsupported duration format: {!r}".format(text))
    total = 0
    for unit, amount in match.groupdict().items():
        if amount:
            total += int(amount) * UNIT_SECONDS[unit[0]]
    LOG.debug("parsed duration %r as %d seconds", text, total)
    return float(total)


def format_duration(seconds: float) -> str:
    """Render seconds back into the compact ``1h30m`` notation."""
    remaining = int(max(0, seconds))
    parts = []
    for unit in ("d", "h", "m", "s"):
        size = UNIT_SECONDS[unit]
        if remaining >= size:
            count, remaining = divmod(remaining, size)
            parts.append("{}{}".format(count, unit))
    return "".join(parts) or "0s"


__all__ = ["DURATION_PATTERN", "UNIT_SECONDS", "parse_duration", "format_duration"]
