"""Compose metric names under a consistent hierarchical namespace.

Different collectors historically used ad-hoc prefixes, which fragmented
dashboards.  A namespace builder enforces the ``vm.<domain>.<metric>``
layout without repeating string formatting at every call site.
"""

import logging
import re

LOG = logging.getLogger(__name__)

INVALID_PATTERN = re.compile(r"[^a-z0-9_.]")


def sanitize_part(part):
    """Normalise a namespace component to lowercase snake style."""
    cleaned = INVALID_PATTERN.sub("_", str(part).strip().lower()).strip("_")
    if not cleaned:
        raise ValueError("namespace components must not be empty")
    return cleaned


def build_name(*parts):
    """Join components into a dotted metric name."""
    components = [sanitize_part(part) for part in parts]
    name = ".".join(components)
    LOG.debug("built metric name %s", name)
    return name


def belongs_to(name, namespace):
    """Return True when the metric name lives under the namespace."""
    prefix = sanitize_part(namespace) + "."
    return str(name).startswith(prefix)


def shorten(name, limit=200):
    """Truncate pathologically long metric names at a component boundary."""
    text = str(name)
    if len(text) <= limit:
        return text
    LOG.warning("metric name exceeds %d characters and was truncated", limit)
    return text[:limit].rsplit(".", 1)[0]
