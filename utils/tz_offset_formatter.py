"""Format timezone offsets for display.

Turns a signed number of seconds into the compact +05:30 style label used in
logs and UI badges, and parses such labels back to seconds.
"""
import logging

LOG = logging.getLogger(__name__)


def format_offset(offset_seconds):
    """Render a signed offset in seconds as a plus or minus HH:MM label."""
    total = int(offset_seconds)
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    hours, rem = divmod(total, 3600)
    minutes = rem // 60
    return "%s%02d:%02d" % (sign, hours, minutes)


def parse_offset(label):
    """Parse an HH:MM offset label back into seconds."""
    text = label.strip()
    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("+-")
    hours_text, _, minutes_text = text.partition(":")
    seconds = int(hours_text) * 3600 + int(minutes_text) * 60
    return sign * seconds


__all__ = ["format_offset", "parse_offset"]
