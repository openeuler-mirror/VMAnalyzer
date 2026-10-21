"""Format rows as a GitHub-flavoured Markdown table with alignment.

Report generators emit tables consumed by issue trackers.  Escaping pipes
and computing column widths keeps the table renderable even when cell
content contains arbitrary text.
"""

import logging
from typing import Iterable, List, Sequence

LOG = logging.getLogger(__name__)

ALIGNMENTS = {"left": ":---", "right": "---:", "center": ":---:"}


def escape_cell(value: object) -> str:
    """Escape pipe characters and newlines inside a table cell."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def render_table(headers: Sequence[str], rows: Iterable[Sequence[object]],
                 align: str = "left") -> List[str]:
    """Return Markdown table lines with padded columns."""
    marker = ALIGNMENTS.get(align, ALIGNMENTS["left"])
    cells = [[escape_cell(value) for value in row] for row in rows]
    widths = [len(str(header)) for header in headers]
    for row in cells:
        for index, value in enumerate(row[:len(widths)]):
            widths[index] = max(widths[index], len(value))
    lines = ["| " + " | ".join(str(header).ljust(widths[index])
                               for index, header in enumerate(headers)) + " |"]
    lines.append("| " + " | ".join(marker.ljust(widths[index])
                                   for index in range(len(headers))) + " |")
    for row in cells:
        padded = [row[index].ljust(widths[index]) if index < len(row)
                  else " " * widths[index] for index in range(len(headers))]
        lines.append("| " + " | ".join(padded) + " |")
    LOG.debug("rendered Markdown table with %d row(s)", len(cells))
    return lines


__all__ = ["ALIGNMENTS", "escape_cell", "render_table"]
