"""Highlight search terms inside text with configurable markers."""
import re

__all__ = ["highlight_terms", "highlight_lines", "highlight_ranges"]


def highlight_terms(text, terms, prefix="[", suffix="]", case_sensitive=False):
    """Wrap every occurrence of *terms* in *text* with marker strings."""
    words = [re.escape(str(t)) for t in terms if str(t)]
    if not words:
        return str(text)
    pattern = re.compile("(" + "|".join(words) + ")", 0 if case_sensitive else re.IGNORECASE)
    return pattern.sub(lambda m: "%s%s%s" % (prefix, m.group(0), suffix), str(text))


def highlight_lines(lines, terms, **kwargs):
    """Apply :func:`highlight_terms` to each line in *lines*."""
    return [highlight_terms(line, terms, **kwargs) for line in lines]


def highlight_ranges(text, terms, case_sensitive=False):
    """Return ``(start, end)`` spans of the matched terms in *text*."""
    words = [re.escape(str(t)) for t in terms if str(t)]
    if not words:
        return []
    pattern = re.compile("|".join(words), 0 if case_sensitive else re.IGNORECASE)
    return [match.span() for match in pattern.finditer(str(text))]
