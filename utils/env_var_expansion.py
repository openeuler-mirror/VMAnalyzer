"""Expand ``${VAR}`` and ``$VAR`` references inside strings using a mapping."""

import re

_REFERENCE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)")
_MAX_DEPTH = 10


def _lookup(name, mapping, default):
    """Return the substitution for ``name`` or a fallback marker."""
    value = mapping.get(name)
    return default if value is None else str(value)


def expand(text, mapping, default=""):
    """Expand variable references, leaving unresolvable ones as ``default``."""
    def replace(match):
        name = match.group(1) or match.group(2)
        return _lookup(name, mapping, default)

    result = text or ""
    for _ in range(_MAX_DEPTH):
        updated = _REFERENCE.sub(replace, result)
        if updated == result:
            break
        result = updated
    return result


def used_variables(text):
    """Return the sorted distinct variable names referenced in the text."""
    return sorted({m.group(1) or m.group(2) for m in _REFERENCE.finditer(text or "")})


__all__ = ["expand", "used_variables"]
