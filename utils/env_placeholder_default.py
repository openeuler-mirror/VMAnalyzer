"""Resolve ``${VAR:-default}`` placeholders in configuration strings.

Container manifests frequently embed shell-style defaults in environment
values.  Python does not expand them, so a small resolver prevents literal
placeholder text from leaking into generated commands.
"""

import logging
import os
import re
from typing import Mapping, Optional

LOG = logging.getLogger(__name__)

PLACEHOLDER_PATTERN = re.compile(r"\$\{(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?::-(?P<default>[^}]*))?\}")


def resolve(text: str, env: Optional[Mapping[str, str]] = None) -> str:
    """Replace placeholders with environment values or inline defaults."""
    source = os.environ if env is None else env
    missing = []

    def replace(match: "re.Match") -> str:
        name = match.group("name")
        default = match.group("default")
        if name in source and source[name] != "":
            return source[name]
        if default is not None:
            return default
        missing.append(name)
        return ""

    resolved = PLACEHOLDER_PATTERN.sub(replace, text)
    if missing:
        LOG.warning("unresolved placeholder(s): %s", ", ".join(sorted(set(missing))))
    return resolved


def find_placeholders(text: str) -> list:
    """Return the variable names referenced by *text*."""
    return [match.group("name") for match in PLACEHOLDER_PATTERN.finditer(text)]


__all__ = ["PLACEHOLDER_PATTERN", "resolve", "find_placeholders"]
