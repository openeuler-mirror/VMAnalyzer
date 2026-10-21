"""Group large numbers with separators while preserving precision.

Capacity reports are hard to scan when byte counts appear as long digit
strings.  Grouping by thousands with an explicit separator makes values
verifiable at a glance without changing their numeric meaning.
"""

import logging
from typing import Optional

LOG = logging.getLogger(__name__)


def group_number(value, separator: str = ",", precision: Optional[int] = None) -> str:
    """Return the value with grouped integer digits."""
    if precision is not None:
        text = "{:,.{}f}".format(float(value), precision)
        return text.replace(",", "\x00").replace(separator, "") if separator != "," else text
    try:
        number = int(value)
    except (TypeError, ValueError):
        LOG.warning("cannot group non-numeric value %r", value)
        return str(value)
    sign = "-" if number < 0 else ""
    digits = str(abs(number))
    chunks = []
    while digits:
        chunks.append(digits[-3:])
        digits = digits[:-3]
    grouped = separator.join(reversed(chunks)) or "0"
    return sign + grouped


def group_with_unit(value: int, separator: str = ",") -> str:
    """Group an integer and append the magnitude suffix."""
    units = ((10 ** 9, "G"), (10 ** 6, "M"), (10 ** 3, "K"))
    for size, suffix in units:
        if abs(value) >= size:
            return "{:.2f}{}".format(value / size, suffix)
    return group_number(value, separator)


__all__ = ["group_number", "group_with_unit"]
