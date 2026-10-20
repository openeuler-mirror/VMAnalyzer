"""Render rows of cells as a simple aligned plain-text table."""
__all__ = ["render_table", "column_widths"]


def column_widths(rows, padding=1):
    """Return the maximum content length of each column plus padding."""
    if not rows:
        return []
    columns = max(len(row) for row in rows)
    widths = [0] * columns
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(str(cell)))
    return [w + padding for w in widths]


def render_table(rows, pager="|", padding=1):
    """Return a list of text lines forming an aligned table."""
    widths = column_widths(rows, padding)
    lines = []
    for row in rows:
        cells = [str(c).ljust(widths[i]) for i, c in enumerate(row)]
        lines.append((" " + pager + " ").join(cells).rstrip())
    return lines
