"""Truncate strings to a maximum length using an ellipsis marker."""
__all__ = ["truncate", "truncate_middle", "truncate_words"]


def truncate(text, limit, marker="..."):
    """Shorten *text* to at most *limit* characters including *marker*."""
    text = str(text)
    if limit <= len(marker):
        return marker[:limit]
    if len(text) <= limit:
        return text
    return text[: limit - len(marker)].rstrip() + marker


def truncate_middle(text, limit, marker="..."):
    """Shorten *text*, keeping both the start and the end visible."""
    text = str(text)
    if len(text) <= limit or limit <= len(marker):
        return truncate(text, limit, marker)
    keep = limit - len(marker)
    head = keep - keep // 2
    return text[:head] + marker + text[len(text) - (keep - head):]


def truncate_words(text, limit, marker="..."):
    """Drop trailing whole words until the result fits within *limit*."""
    text = str(text)
    if len(text) <= limit:
        return text
    cut = text[: limit - len(marker)].rsplit(" ", 1)[0]
    return cut + marker
