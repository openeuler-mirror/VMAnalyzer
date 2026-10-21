"""Render horizontal ASCII bar charts for terminal reports.

Plotting libraries are unavailable on many hypervisors, but a monospace bar
chart still communicates relative magnitudes well inside ssh sessions.
"""

import logging
from typing import Iterable, List, Tuple

LOG = logging.getLogger(__name__)


def render_bars(rows: Iterable[Tuple[str, float]], width: int = 40,
                char: str = "#") -> List[str]:
    """Return one bar line per row, scaled to the largest value."""
    items = list(rows)
    if not items:
        LOG.debug("no rows supplied to the bar chart")
        return []
    peak = max(value for _, value in items) or 1.0
    label_width = max(len(str(label)) for label, _ in items)
    lines: List[str] = []
    for label, value in items:
        filled = int(round(max(0.0, value) / peak * width))
        lines.append("{} | {}{} {:g}".format(str(label).ljust(label_width),
                                             char * filled,
                                             " " * (width - filled), value))
    LOG.debug("rendered %d bar(s) at width %d", len(lines), width)
    return lines


def sparkline(values: Iterable[float]) -> str:
    """Return a single-line sparkline using block characters."""
    blocks = " .:-=+*#%@"
    sample = [float(value) for value in values]
    if not sample:
        return ""
    peak = max(sample) or 1.0
    return "".join(blocks[min(len(blocks) - 1, int(value / peak * (len(blocks) - 1)))]
                   for value in sample)


__all__ = ["render_bars", "sparkline"]
