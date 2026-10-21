"""Cosine similarity for sparse vectors stored as index-value maps.

Feature vectors for VM behaviour are usually sparse, and dense conversion
wastes memory once dimensions grow past a few thousand.  This helper walks
the smaller map only and skips zero entries entirely.
"""

import logging
import math
from typing import Dict, Mapping

LOG = logging.getLogger(__name__)


def dot_product(left: Mapping[int, float], right: Mapping[int, float]) -> float:
    """Return the dot product of two sparse vectors."""
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(index, 0.0) for index, value in left.items())


def norm(vector: Mapping[int, float]) -> float:
    """Return the Euclidean norm of a sparse vector."""
    return math.sqrt(sum(float(value) ** 2 for value in vector.values()))


def cosine_similarity(left: Mapping[int, float],
                      right: Mapping[int, float]) -> float:
    """Return the cosine similarity, or zero when either vector is empty."""
    left_norm, right_norm = norm(left), norm(right)
    if left_norm == 0.0 or right_norm == 0.0:
        LOG.debug("zero norm encountered, similarity is undefined")
        return 0.0
    return dot_product(left, right) / (left_norm * right_norm)


def top_dimensions(vector: Mapping[int, float], limit: int = 5) -> Dict[int, float]:
    """Return the largest magnitude dimensions of a sparse vector."""
    ordered = sorted(vector.items(), key=lambda item: abs(item[1]), reverse=True)
    return dict(ordered[: max(0, limit)])


__all__ = ["dot_product", "norm", "cosine_similarity", "top_dimensions"]
