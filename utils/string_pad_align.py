"""Pad and align strings for fixed-width plain-text layouts."""
__all__ = ["pad_right", "pad_left", "pad_center", "column_block", "pad_both", "pad_widths"]


def pad_right(text, width, fill=" "):
    """Left-align *text* within *width* columns."""
    return str(text).ljust(width, fill[0])


def pad_left(text, width, fill=" "):
    """Right-align *text* within *width* columns."""
    return str(text).rjust(width, fill[0])


def pad_center(text, width, fill=" "):
    """Centre *text* within *width* columns."""
    return str(text).center(width, fill[0])


def column_block(rows, widths):
    """Format *rows* of cells into aligned fixed-width columns."""
    return ["".join(pad_right(c, w) for c, w in zip(row, widths)) for row in rows]


def pad_both(text, left_width, right_width, fill=" "):
    """Pad *text* with leading and trailing fill of the given widths."""
    return fill[0] * left_width + str(text) + fill[0] * right_width


def pad_widths(rows, fill=" "):
    """Pad every row to the widest cell count using *fill*."""
    width = max((len(r) for r in rows), default=0)
    return [list(r) + [fill] * (width - len(r)) for r in rows]
