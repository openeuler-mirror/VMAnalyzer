"""Title-case text while keeping small connector words lowercase."""
__all__ = ["title_case", "title_case_lines", "SMALL_WORDS"]

SMALL_WORDS = frozenset({
    "a", "an", "and", "as", "at", "but", "by", "for", "in", "nor",
    "of", "on", "or", "per", "the", "to", "via", "vs",
})


def title_case(text, small_words=SMALL_WORDS):
    """Capitalise each word except small ones that are not first or last."""
    words = str(text).split()
    out = []
    for idx, word in enumerate(words):
        core = word.lower()
        if idx in (0, len(words) - 1) or core not in small_words:
            out.append(core.capitalize())
        else:
            out.append(core)
    return " ".join(out)


def title_case_lines(lines):
    """Apply :func:`title_case` to every line in *lines*."""
    return [title_case(line) for line in lines]
