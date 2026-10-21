"""Render a bordered ASCII table with rounded separators.

Bordered tables are easier to paste into plain-text incident notes because
column boundaries remain visible even after reflow.  Widths are derived
from the content rather than hard-coded.
"""

import logging
from typing import Iterable, List, Sequence

LOG = logging.getLogger(__name__)


def render(headers: Sequence[str], rows: Iterable[Sequence[object]]) -> List[str]:
    """Return a bordered table with aligned columns."""
    cells = [[str(value) for value in row] for row in rows]
    widths = [len(str(header)) for header in headers]
    for row in cells:
        for index, value in enumerate(row[:len(widths)]):
            widths[index] = max(widths[index], len(value))
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def format_row(values: Sequence[str]) -> str:
        padded = [values[index].ljust(widths[index]) if index < len(values)
                  else " " * widths[index] for index in range(len(widths))]
        return "| " + " | ".join(padded) + " |"

    lines = [border, format_row([str(header) for header in headers]), border]
    lines.extend(format_row(row) for row in cells)
    lines.append(border)
    LOG.debug("rendered ASCII table with %d row(s)", len(cells))
    return lines


def plain(headers: Sequence[str], rows: Iterable[Sequence[object]]) -> str:
    """Return the bordered table as a single newline joined string."""
    return "\n".join(render(headers, rows))


__all__ = ["render", "plain"]
