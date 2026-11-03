"""Render rtc irq values for the plain text reports.

Operators read these reports in a terminal, so raw floats and byte counts are
hard to scan.  The helpers format durations, sizes and aligned columns
consistently across every report.
"""

import logging

LOG = logging.getLogger(__name__)

UNITS = ("B", "KiB", "MiB", "GiB", "TiB")


def human_bytes(value):
    """Format a byte count with the largest unit that keeps it readable."""
    number = float(value)
    for unit in UNITS:
        if abs(number) < 1024.0 or unit == UNITS[-1]:
            return "%.1f %s" % (number, unit)
        number /= 1024.0
    return "%.1f %s" % (number, UNITS[-1])


def human_duration(seconds):
    """Format seconds as ``Xd Yh Zm`` dropping leading zero parts."""
    total = int(round(float(seconds)))
    days, rest = divmod(total, 86400)
    hours, rest = divmod(rest, 3600)
    minutes, secs = divmod(rest, 60)
    parts = []
    if days:
        parts.append("%dd" % days)
    if hours:
        parts.append("%dh" % hours)
    if minutes:
        parts.append("%dm" % minutes)
    if secs or not parts:
        parts.append("%ds" % secs)
    return " ".join(parts)


def align_columns(rows):
    """Pad every column to its widest cell and join rows into text."""
    if not rows:
        return ""
    widths = [0] * max(len(row) for row in rows)
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(str(cell)))
    return "\n".join(
        " ".join(str(cell).ljust(widths[index])
                 for index, cell in enumerate(row))
        for row in rows
    )


__all__ = ["human_bytes", "human_duration", "align_columns"]
