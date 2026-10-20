"""Detect the naming convention used by an identifier string."""
import re

__all__ = ["detect_case_style", "is_consistent", "CASE_STYLES"]

CASE_STYLES = ("snake", "kebab", "camel", "pascal", "upper_snake", "unknown")


def detect_case_style(name):
    """Classify *name* into one of the recognised case styles."""
    text = str(name)
    if not text:
        return "unknown"
    if re.fullmatch(r"[a-z0-9]+(_[a-z0-9]+)+", text):
        return "snake"
    if re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)+", text):
        return "kebab"
    if re.fullmatch(r"[A-Z0-9]+(_[A-Z0-9]+)+", text):
        return "upper_snake"
    if re.fullmatch(r"[a-z][A-Za-z0-9]*", text):
        return "camel"
    if re.fullmatch(r"[A-Z][A-Za-z0-9]*", text):
        return "pascal"
    return "unknown"


def is_consistent(names):
    """Return True when every name shares one non-unknown style."""
    styles = {detect_case_style(n) for n in names}
    return len(styles) == 1 and "unknown" not in styles
