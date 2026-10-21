"""Count lines in a text file without loading it into memory.

Large guest journals can exceed available agent memory.  Reading fixed size
blocks and counting newline bytes keeps the peak footprint constant while
still handling files that do not end with a newline.
"""

import logging
from typing import Optional

LOG = logging.getLogger(__name__)

CHUNK_SIZE = 1024 * 1024


def count_lines(path: str, chunk_size: int = CHUNK_SIZE,
                encoding: str = "utf-8") -> int:
    """Return the number of lines in *path*, counting a trailing partial line."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    total = 0
    last_byte = b"\n"
    with open(path, "rb") as handle:
        while True:
            block = handle.read(chunk_size)
            if not block:
                break
            total += block.count(b"\n")
            last_byte = block[-1:]
    if last_byte != b"\n":
        total += 1
    LOG.debug("counted %d line(s) in %s", total, path)
    return total


def count_lines_safe(path: str, limit: int = 10_000_000) -> Optional[int]:
    """Count lines but stop early once *limit* is exceeded, returning None."""
    seen = 0
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(CHUNK_SIZE), b""):
            seen += block.count(b"\n")
            if seen > limit:
                LOG.warning("line count for %s exceeded the limit of %d", path, limit)
                return None
    return seen


__all__ = ["CHUNK_SIZE", "count_lines", "count_lines_safe"]
