"""Join URI path segments without duplicating or dropping slashes.

API clients that concatenate base URLs and resource paths frequently
produce ``//`` or lose the leading slash.  This helper normalises both
sides while preserving an optional query string.
"""

import logging
from typing import Iterable

LOG = logging.getLogger(__name__)


def split_query(uri: str):
    """Split a URI into its path and query parts."""
    path, separator, query = uri.partition("?")
    return path, (separator + query if separator else "")


def join_path(base: str, *segments: str) -> str:
    """Join path segments with exactly one separating slash."""
    path, query = split_query(base)
    parts = [part for part in path.split("/") if part]
    for segment in segments:
        for piece in str(segment).split("/"):
            if piece:
                parts.append(piece)
    trailing = path.endswith("/") and not any(segments)
    joined = "/" + "/".join(parts)
    if not parts:
        joined = "/"
    elif trailing:
        joined += "/"
    LOG.debug("joined path into %s", joined)
    return joined + query


def join_many(base: str, segments: Iterable[str]) -> str:
    """Join an iterable of segments onto a base URI."""
    return join_path(base, *list(segments))


__all__ = ["split_query", "join_path", "join_many"]
