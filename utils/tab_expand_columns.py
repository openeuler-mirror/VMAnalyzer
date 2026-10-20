"""Expand tab characters using explicit display column stops."""
import textwrap

__all__ = ["expand_tabs", "display_columns", "tabs_to_spaces"]


def expand_tabs(text, tab_size=4):
    """Dedent *text* and expand its tabs using fixed *tab_size* stops."""
    return textwrap.dedent(str(text)).expandtabs(tab_size)


def display_columns(text, tab_size=4, start=0):
    """Compute the visual end column of *text* after tab expansion."""
    column = start
    for ch in str(text):
        if ch == "\t":
            column += tab_size - (column % tab_size)
        else:
            column += 1
    return column


def tabs_to_spaces(text, tab_size=4):
    """Return *text* with every tab replaced by the matching spaces."""
    return str(text).expandtabs(tab_size)
