"""Sparse vector dot product over index dictionaries.

Vectors are represented as ``{index: coefficient}`` maps, so the dot product
only touches indices present in both operands.  Iterating the shorter map is
the cheapest way to build that intersection without scanning dense arrays.
"""

import logging
from typing import Dict, Iterable, Tuple

LOG = logging.getLogger(__name__)

SparseVector = Dict[int, float]


def dot_product(left: SparseVector, right: SparseVector) -> float:
    """Return the dot product, walking the smaller operand's indices."""
    if len(left) > len(right):
        left, right = right, left
    total = 0.0
    for index, coefficient in left.items():
        other = right.get(index)
        if other is not None:
            total += coefficient * other
    LOG.debug("dot over %d shared candidates", len(left))
    return total


def add_scaled(target: SparseVector, source: SparseVector, scale: float) -> None:
    """Accumulate ``source * scale`` into *target* in place, dropping zeros."""
    for index, coefficient in source.items():
        updated = target.get(index, 0.0) + coefficient * scale
        if updated:
            target[index] = updated
        else:
            target.pop(index, None)


def cosine_similarity(left: SparseVector, right: SparseVector) -> float:
    """Return the cosine similarity of two sparse vectors, or 0.0."""
    numerator = dot_product(left, right)
    left_norm = sum(value * value for value in left.values()) ** 0.5
    right_norm = sum(value * value for value in right.values()) ** 0.5
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def largest_entries(vector: SparseVector, limit: int) -> Iterable[Tuple[int, float]]:
    """Return the *limit* highest-magnitude entries as pairs."""
    ranked = sorted(vector.items(), key=lambda item: abs(item[1]), reverse=True)
    return ranked[:limit]


__all__ = ["dot_product", "add_scaled", "cosine_similarity", "largest_entries"]
