"""Rename INI sections while preserving comments and key order.

Configuration migrations rename sections such as ``[vm]`` to ``[guest]``.
Rewriting with configparser loses comments, so the helper performs a
line-oriented rename that touches only matching headers.
"""

import logging
import re
from typing import Dict, Iterable, List

LOG = logging.getLogger(__name__)

SECTION_PATTERN = re.compile(r"^(?P<indent>\s*)\[(?P<name>[^\]]+)\](?P<tail>\s*)$")


def rename_sections(lines: Iterable[str], mapping: Dict[str, str]) -> List[str]:
    """Rename configured sections and keep every other line untouched."""
    output: List[str] = []
    renamed = 0
    for line in lines:
        match = SECTION_PATTERN.match(line.rstrip("\n"))
        if match and match.group("name") in mapping:
            ending = "\n" if line.endswith("\n") else ""
            output.append("{}[{}]{}{}".format(match.group("indent"),
                                              mapping[match.group("name")],
                                              match.group("tail"), ending))
            renamed += 1
            continue
        output.append(line)
    LOG.debug("renamed %d section header(s)", renamed)
    return output


def list_sections(lines: Iterable[str]) -> List[str]:
    """Return section names in file order."""
    names: List[str] = []
    for line in lines:
        match = SECTION_PATTERN.match(line.rstrip("\n"))
        if match:
            names.append(match.group("name").strip())
    return names


def find_duplicates(lines: Iterable[str]) -> List[str]:
    """Return section names that appear more than once."""
    seen = set()
    duplicates = []
    for name in list_sections(lines):
        if name in seen and name not in duplicates:
            duplicates.append(name)
        seen.add(name)
    if duplicates:
        LOG.warning("duplicate INI section(s): %s", ", ".join(duplicates))
    return duplicates


__all__ = ["SECTION_PATTERN", "rename_sections", "list_sections", "find_duplicates"]
