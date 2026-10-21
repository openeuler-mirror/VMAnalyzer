"""Convert a numeric series into a compact block sparkline string.

Sparklines fit a trend into a table cell, which is valuable when the full
chart would not fit the terminal.  Missing values become a visual gap
instead of a misleading zero.
"""

import logging
from typing import Iterable, Optional

LOG = logging.getLogger(__name__)

LEVELS = "▁▂▃▄▅▆▇█"


def sparkline(values: Iterable[Optional[float]], gap: str = " ") -> str:
    """Return a sparkline where None values render as *gap*."""
    sample = list(values)
    present = [float(value) for value in sample if value is not None]
    if not present:
        return gap * len(sample)
    low, high = min(present), max(present)
    span = high - low
    characters = []
    for value in sample:
        if value is None:
            characters.append(gap)
            continue
        position = 0 if span == 0 else int((float(value) - low) / span * (len(LEVELS) - 1))
        characters.append(LEVELS[min(len(LEVELS) - 1, position)])
    rendered = "".join(characters)
    LOG.debug("rendered sparkline of %d point(s)", len(sample))
    return rendered


def with_bounds(values: Iterable[Optional[float]]) -> str:
    """Return a sparkline prefixed by its value range."""
    sample = list(values)
    present = [value for value in sample if value is not None]
    if not present:
        return sparkline(sample)
    return "{}..{} {}".format(round(min(present), 2), round(max(present), 2),
                              sparkline(sample))


__all__ = ["LEVELS", "sparkline", "with_bounds"]
