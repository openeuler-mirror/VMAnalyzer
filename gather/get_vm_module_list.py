"""Parse the text interface that exposes module list counters.

Procfs style output is either ``key value`` or ``key: value``.  The parser
accepts both shapes so gather scripts stop carrying their own copy of this
logic and drifting apart.
"""

import logging

LOG = logging.getLogger(__name__)


def parse_lines(text):
    """Return a mapping built from key/value lines, skipping comments."""
    data = {}
    for line in (text or "").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace(":", " ").split()
        if len(parts) < 2:
            continue
        data[parts[0]] = parts[1]
    LOG.debug("parsed %d module_list entries", len(data))
    return data


def as_int(data, key, default=0):
    """Read *key* as an integer, falling back to *default* on bad input."""
    try:
        return int(data.get(key, default))
    except (TypeError, ValueError):
        LOG.warning("non integer module_list value for %s", key)
        return default


def as_float(data, key, default=0.0):
    """Read *key* as a float, falling back to *default* on bad input."""
    try:
        return float(data.get(key, default))
    except (TypeError, ValueError):
        LOG.warning("non numeric module_list value for %s", key)
        return default


def require(data, keys):
    """Return the subset of *keys* present in *data* and the missing ones."""
    present = {key: data[key] for key in keys if key in data}
    missing = [key for key in keys if key not in data]
    if missing:
        LOG.info("missing module_list fields: %s", ",".join(missing))
    return present, missing


__all__ = ["parse_lines", "as_int", "as_float", "require"]
