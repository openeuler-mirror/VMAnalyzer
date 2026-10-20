"""Diff two token sequences using a longest-common-subsequence pass."""
from collections import namedtuple

__all__ = ["diff_tokens", "DiffOp"]

DiffOp = namedtuple("DiffOp", "op token")


def diff_tokens(before, after):
    """Return ordered insert/delete/equal operations between two token lists."""
    a, b = list(before), list(after)
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) - 1, -1, -1):
        for j in range(len(b) - 1, -1, -1):
            if a[i] == b[j]:
                table[i][j] = table[i + 1][j + 1] + 1
            else:
                table[i][j] = max(table[i + 1][j], table[i][j + 1])
    ops, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            ops.append(DiffOp("equal", a[i]))
            i += 1
            j += 1
        elif table[i + 1][j] >= table[i][j + 1]:
            ops.append(DiffOp("delete", a[i]))
            i += 1
        else:
            ops.append(DiffOp("insert", b[j]))
            j += 1
    ops.extend(DiffOp("delete", token) for token in a[i:])
    ops.extend(DiffOp("insert", token) for token in b[j:])
    return ops
