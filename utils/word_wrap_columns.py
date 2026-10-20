"""Wrap paragraphs of text to a fixed maximum column width."""
import textwrap

__all__ = ["wrap_columns", "wrap_preserving_paragraphs", "wrap_lines", "indent_wrapped"]


def wrap_columns(text, width=72, initial=None, subsequent=None):
    """Wrap *text* to *width* columns with optional hanging indents."""
    return textwrap.fill(
        str(text),
        width=width,
        initial_indent=initial or "",
        subsequent_indent=subsequent or "",
    )


def wrap_preserving_paragraphs(text, width=72):
    """Wrap text while keeping blank-line separated paragraphs distinct."""
    blocks = str(text).split("\n\n")
    return "\n\n".join(textwrap.fill(b, width=width) for b in blocks)


def wrap_lines(lines, width=72):
    """Wrap each line in *lines* to at most *width* columns."""
    wrapped = []
    for line in lines:
        wrapped.extend(textwrap.wrap(str(line), width=width) or [""])
    return wrapped


def indent_wrapped(text, width=72, indent="    "):
    """Wrap *text* and prefix every resulting line with *indent*."""
    return textwrap.fill(
        str(text), width=width, initial_indent=indent, subsequent_indent=indent
    )
