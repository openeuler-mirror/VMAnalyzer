"""Produce a compact unified diff between two line sequences.

Full diff tooling is unnecessary when comparing short configuration or
report fragments.  This implementation uses a longest common subsequence to
mark additions and removals with a configurable context size.
"""

import logging
from typing import List, Sequence, Tuple

LOG = logging.getLogger(__name__)

Op = Tuple[str, int, int]


def lcs_ops(left: Sequence[str], right: Sequence[str]) -> List[Op]:
    """Return ``(kind, left_index, right_index)`` edit operations."""
    rows, columns = len(left), len(right)
    table = [[0] * (columns + 1) for _ in range(rows + 1)]
    for i in range(rows - 1, -1, -1):
        for j in range(columns - 1, -1, -1):
            if left[i] == right[j]:
                table[i][j] = table[i + 1][j + 1] + 1
            else:
                table[i][j] = max(table[i + 1][j], table[i][j + 1])
    ops: List[Op] = []
    i = j = 0
    while i < rows and j < columns:
        if left[i] == right[j]:
            ops.append((" ", i, j))
            i += 1
            j += 1
        elif table[i + 1][j] >= table[i][j + 1]:
            ops.append(("-", i, -1))
            i += 1
        else:
            ops.append(("+", -1, j))
            j += 1
    while i < rows:
        ops.append(("-", i, -1))
        i += 1
    while j < columns:
        ops.append(("+", -1, j))
        j += 1
    LOG.debug("computed %d edit operation(s)", len(ops))
    return ops


def render(left: Sequence[str], right: Sequence[str]) -> List[str]:
    """Render operations as unified-diff style lines."""
    lines: List[str] = []
    for kind, left_index, right_index in lcs_ops(left, right):
        if kind == "+":
            lines.append("+ " + right[right_index])
        elif kind == "-":
            lines.append("- " + left[left_index])
        else:
            lines.append("  " + left[left_index])
    return lines


__all__ = ["Op", "lcs_ops", "render"]
