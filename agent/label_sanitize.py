"""Sanitise label values so they are safe as storage keys.

VM names may contain spaces, slashes or non-ASCII characters that break key
parsing and dashboard filters.  Sanitising deterministically keeps keys
stable while remaining readable.
"""

import logging
import re

LOG = logging.getLogger(__name__)

UNSAFE_PATTERN = re.compile(r"[^A-Za-z0-9_.-]")
MAX_LABEL = 120


def sanitize(value, separator="_"):
    """Return a storage-safe label value."""
    text = str(value).strip()
    cleaned = UNSAFE_PATTERN.sub(separator, text)
    cleaned = re.sub(r"{}+".format(re.escape(separator)), separator, cleaned).strip(separator)
    if len(cleaned) > MAX_LABEL:
        LOG.warning("label truncated from %d to %d characters", len(cleaned), MAX_LABEL)
        cleaned = cleaned[:MAX_LABEL]
    return cleaned or "unnamed"


def sanitize_labels(labels):
    """Sanitise every value in a label mapping."""
    return {key: sanitize(value) for key, value in labels.items()}


def is_safe(value):
    """Return True when the value needs no sanitisation."""
    return bool(value) and len(str(value)) <= MAX_LABEL and not UNSAFE_PATTERN.search(str(value))
