"""Convert Java-style properties text into nested JSON-ready mappings.

Legacy exporters emit dotted keys such as ``vm.disk.0.size=20``.  Expanding
them into nested dicts makes the payload directly serialisable and lets
report templates address fields without string splitting.
"""

import logging
from typing import Dict, List, Tuple

LOG = logging.getLogger(__name__)

ESCAPES = {"t": "\t", "n": "\n", "r": "\r", "\\": "\\", "=": "=", ":": ":"}


def parse_line(line: str) -> Tuple[str, str]:
    """Split a properties line into key and value."""
    stripped = line.strip()
    if not stripped or stripped[0] in "#!":
        return "", ""
    index = 0
    key_chars: List[str] = []
    while index < len(stripped):
        char = stripped[index]
        if char == "\\" and index + 1 < len(stripped):
            key_chars.append(ESCAPES.get(stripped[index + 1], stripped[index + 1]))
            index += 2
            continue
        if char in "=:":
            break
        key_chars.append(char)
        index += 1
    value = stripped[index + 1:].strip() if index < len(stripped) else ""
    return "".join(key_chars).strip(), value


def to_nested(lines: List[str], separator: str = ".") -> Dict[str, object]:
    """Expand dotted keys into nested dictionaries."""
    root: Dict[str, object] = {}
    for line in lines:
        key, value = parse_line(line)
        if not key:
            continue
        parts = key.split(separator)
        cursor = root
        for part in parts[:-1]:
            nxt = cursor.setdefault(part, {})
            if not isinstance(nxt, dict):
                nxt = {}
                cursor[part] = nxt
            cursor = nxt
        cursor[parts[-1]] = value
    LOG.debug("converted %d line(s) into nested properties", len(lines))
    return root


__all__ = ["ESCAPES", "parse_line", "to_nested"]
