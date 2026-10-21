"""Overlay environment overrides onto a configuration mapping.

Deployments need to tweak a few settings without rewriting config files.
Using a fixed prefix and double underscores for nesting keeps overrides
predictable and avoids collisions with unrelated variables.
"""

import logging
import os
from typing import Dict, Mapping, Optional

LOG = logging.getLogger(__name__)


def overlay_env(config: Dict[str, object], prefix: str = "VMA_",
                separator: str = "__", env: Optional[Mapping[str, str]] = None) -> Dict[str, object]:
    """Return a copy of *config* with matching environment values applied."""
    source = os.environ if env is None else env
    result: Dict[str, object] = {}
    for key, value in config.items():
        result[key] = dict(value) if isinstance(value, dict) else value
    applied = 0
    for name, value in source.items():
        if not name.startswith(prefix):
            continue
        path = name[len(prefix):].lower().split(separator)
        cursor = result
        for part in path[:-1]:
            nxt = cursor.get(part)
            if not isinstance(nxt, dict):
                nxt = {}
                cursor[part] = nxt
            cursor = nxt
        cursor[path[-1]] = value
        applied += 1
    if applied:
        LOG.info("applied %d environment override(s)", applied)
    return result


def describe_overrides(prefix: str = "VMA_",
                       env: Optional[Mapping[str, str]] = None) -> Dict[str, str]:
    """List environment variables that would override configuration."""
    source = os.environ if env is None else env
    return {name: value for name, value in source.items() if name.startswith(prefix)}


__all__ = ["overlay_env", "describe_overrides"]
