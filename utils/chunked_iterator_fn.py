"""Yield fixed-size chunks from any iterable without materialising it.

Batch writes to Redis or the report store must respect command size limits.
Chunking lazily keeps memory flat even when the source is a generator over
millions of samples.
"""

import itertools
import logging
from typing import Iterable, Iterator, List, TypeVar

LOG = logging.getLogger(__name__)

T = TypeVar("T")


def chunked(items: Iterable[T], size: int) -> Iterator[List[T]]:
    """Yield lists of at most *size* items."""
    if size <= 0:
        raise ValueError("size must be positive")
    iterator = iter(items)
    emitted = 0
    while True:
        batch = list(itertools.islice(iterator, size))
        if not batch:
            break
        emitted += 1
        yield batch
    LOG.debug("emitted %d chunk(s) of at most %d item(s)", emitted, size)


def chunk_count(total: int, size: int) -> int:
    """Return how many chunks *total* items will produce."""
    if size <= 0:
        raise ValueError("size must be positive")
    return (max(0, total) + size - 1) // size


def flatten(chunks: Iterable[Iterable[T]]) -> Iterator[T]:
    """Rebuild a flat stream from previously chunked data."""
    for batch in chunks:
        for item in batch:
            yield item


__all__ = ["chunked", "chunk_count", "flatten"]
