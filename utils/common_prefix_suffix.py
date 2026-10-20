"""Find the shared prefix and suffix of a collection of strings."""
__all__ = ["common_prefix", "common_suffix", "common_affixes"]


def common_prefix(strings):
    """Return the longest string shared at the start of every input."""
    values = [str(s) for s in strings]
    if not values:
        return ""
    shortest = min(values, key=len)
    for i, ch in enumerate(shortest):
        if any(v[i] != ch for v in values):
            return shortest[:i]
    return shortest


def common_suffix(strings):
    """Return the longest string shared at the end of every input."""
    return common_prefix([str(s)[::-1] for s in strings])[::-1]


def common_affixes(strings):
    """Return the common prefix and suffix as a ``(prefix, suffix)`` pair."""
    return common_prefix(strings), common_suffix(strings)
