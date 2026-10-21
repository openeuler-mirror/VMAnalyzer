"""Check generated file names against filesystem length limits.

Long VM names combined with timestamps easily exceed the 255 byte limit on
ext4, producing truncated names or failed writes.  Checking before writing
lets the collector shorten deterministically.
"""

import logging
from typing import List, Optional

LOG = logging.getLogger(__name__)

MAX_COMPONENT = 255


def encode_length(name: str) -> int:
    """Return the byte length of a name in UTF-8."""
    return len(name.encode("utf-8"))


def problem(name: str, limit: int = MAX_COMPONENT) -> Optional[str]:
    """Return a description when the name is too long or contains a separator."""
    if "/" in name or "\\" in name:
        return "name {!r} contains a path separator".format(name)
    length = encode_length(name)
    if length > limit:
        LOG.warning("file name %r is %d bytes, limit is %d", name, length, limit)
        return "name {!r} is {} bytes, limit is {}".format(name, length, limit)
    return None


def shorten(name: str, limit: int = MAX_COMPONENT, keep_suffix: bool = True) -> str:
    """Return a name shortened safely within the byte limit."""
    if encode_length(name) <= limit:
        return name
    marker = "~"
    if keep_suffix and "." in name:
        stem, _, suffix = name.rpartition(".")
        suffix = "." + suffix
    else:
        stem, suffix = name, ""
    budget = limit - encode_length(marker + suffix)
    truncated = stem.encode("utf-8")[:max(0, budget)].decode("utf-8", errors="ignore")
    result = "{}{}{}".format(truncated, marker, suffix)
    LOG.debug("shortened file name to %d bytes", encode_length(result))
    return result


def check_all(names: List[str], limit: int = MAX_COMPONENT) -> List[str]:
    """Return names that violate the length or separator rules."""
    return [name for name in names if problem(name, limit)]


__all__ = ["MAX_COMPONENT", "encode_length", "problem", "shorten", "check_all"]
