"""Compute set-based similarity between two token collections."""
__all__ = ["jaccard_similarity", "dice_similarity", "overlap_coefficient"]


def _token_set(value):
    """Return the set of lower-cased whitespace tokens in *value*."""
    return set(str(value).lower().split())


def jaccard_similarity(left, right):
    """Return the Jaccard index of the two token sets."""
    a, b = _token_set(left), _token_set(right)
    union = a | b
    return len(a & b) / len(union) if union else 1.0


def dice_similarity(left, right):
    """Return the Sorensen-Dice coefficient of the two token sets."""
    a, b = _token_set(left), _token_set(right)
    total = len(a) + len(b)
    return 2 * len(a & b) / total if total else 1.0


def overlap_coefficient(left, right):
    """Return the overlap coefficient of the two token sets."""
    a, b = _token_set(left), _token_set(right)
    smaller = min(len(a), len(b))
    return len(a & b) / smaller if smaller else 0.0
