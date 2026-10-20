"""Normalise and re-indent blocks of code-like text."""
import textwrap

__all__ = ["dedent_block", "reindent_block", "indent_levels"]


def dedent_block(text):
    """Remove the common leading indentation from every line."""
    return textwrap.dedent(str(text))


def reindent_block(text, width=4, tabs=False):
    """Dedent *text* then re-indent using *width* spaces or tabs."""
    unit = "\t" if tabs else " " * width
    lines = dedent_block(text).splitlines()
    return "\n".join(unit + line if line.strip() else line for line in lines)


def indent_levels(text, tab_width=4):
    """Return the computed indentation level of each non-blank line."""
    levels = []
    for line in str(text).splitlines():
        if not line.strip():
            continue
        expanded = line.expandtabs(tab_width)
        levels.append((len(expanded) - len(expanded.lstrip())) // tab_width)
    return levels
