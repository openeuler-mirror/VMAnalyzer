"""Compare a measured size against configured soft and hard limits."""

WITHIN = "within"
SOFT = "soft-exceeded"
HARD = "hard-exceeded"


def compare_limit(size, soft=None, hard=None):
    """Classify ``size`` against optional soft and hard limits."""
    if hard is not None and size > hard:
        return HARD
    if soft is not None and size > soft:
        return SOFT
    return WITHIN


def breach_ratio(size, limit):
    """Return how far ``size`` exceeds ``limit`` as a ratio (>= 0)."""
    if limit <= 0:
        return float("inf") if size > 0 else 0.0
    return round(max(0.0, size - limit) / limit, 4)


def tightest_limit(size, limits):
    """Return the name of the first limit exceeded from the tightest upwards."""
    ordered = sorted((value, name) for name, value in limits.items() if value is not None)
    for value, name in ordered:
        if size > value:
            return name
    return None


__all__ = ["compare_limit", "breach_ratio", "tightest_limit"]
