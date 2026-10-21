"""Shrink text columns so a table fits a maximum display width.

Terminal reports lose alignment when a single wide column wraps.  Shrinking
proportionally while preserving a minimum width keeps every column readable
and the table within the requested budget.
"""

import logging
from typing import List, Sequence

LOG = logging.getLogger(__name__)


def fit_widths(widths: Sequence[int], total: int, minimum: int = 8) -> List[int]:
    """Return column widths scaled to fit within *total* characters."""
    if total <= 0:
        raise ValueError("total must be positive")
    columns = [max(0, int(width)) for width in widths]
    if not columns:
        return []
    available = total - (len(columns) + 1) * 3
    if sum(columns) <= available:
        return columns
    floors = [min(minimum, width) for width in columns]
    if sum(floors) > available:
        LOG.warning("minimum widths exceed the available space")
        return floors
    extra = available - sum(floors)
    slack = [width - floor for width, floor in zip(columns, floors)]
    total_slack = sum(slack) or 1
    fitted = [floor + int(extra * share / total_slack)
              for floor, share in zip(floors, slack)]
    LOG.debug("fitted %d column(s) into %d characters", len(fitted), available)
    return fitted


def truncate_cell(text: str, width: int) -> str:
    """Trim a cell to *width*, adding an ellipsis when shortened."""
    if width <= 1:
        return text[:max(0, width)]
    return text if len(text) <= width else text[:width - 1] + "…"


__all__ = ["fit_widths", "truncate_cell"]
