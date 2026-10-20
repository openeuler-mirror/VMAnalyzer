"""Parse a single dotenv style ``KEY=VALUE`` line into structured data."""

import re

_LINE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=(.*)$")


def parse_dotenv_line(line):
    """Return ``(key, value)`` with surrounding quotes stripped, or ``None``."""
    stripped = (line or "").strip()
    if not stripped or stripped.startswith("#"):
        return None
    match = _LINE.match(stripped)
    if not match:
        return None
    key, raw = match.group(1), match.group(2).strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        raw = raw[1:-1]
    return key, raw


def parse_dotenv(text):
    """Return an ordered dict built from every valid dotenv line."""
    result = {}
    for line in (text or "").splitlines():
        parsed = parse_dotenv_line(line)
        if parsed:
            result[parsed[0]] = parsed[1]
    return result


def invalid_dotenv_lines(text):
    """Return the 1-based line numbers that fail to parse and are not blank."""
    bad = []
    for index, line in enumerate((text or "").splitlines(), start=1):
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and parse_dotenv_line(line) is None:
            bad.append(index)
    return bad


__all__ = ["parse_dotenv_line", "parse_dotenv", "invalid_dotenv_lines"]
