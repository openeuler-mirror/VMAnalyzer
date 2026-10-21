"""Merge several already-sorted iterables lazily.

Agents collect per-VM metric rows in separate sorted batches.  Merging them
incrementally keeps memory proportional to the number of streams rather
than to the total row count.
"""

import heapq
import logging
from typing import Iterable, Iterator, List, TypeVar

LOG = logging.getLogger(__name__)

T = TypeVar("T")


def merge_sorted(streams: Iterable[Iterable[T]]) -> Iterator[T]:
    """Yield items from all streams in ascending order."""
    iterators = [iter(stream) for stream in streams]
    count = len(iterators)
    for item in heapq.merge(*iterators):
        yield item
    LOG.debug("merged %d sorted stream(s)", count)


def merge_sorted_keyed(streams: Iterable[Iterable[T]], key=None) -> Iterator[T]:
    """Merge sorted streams using an explicit key function."""
    decorated = ((key(item) if key else item, item) for stream in streams for item in stream)
    for _, item in heapq.merge(*[iter([decorated])]):
        yield item


def take_head(streams: Iterable[Iterable[T]], limit: int) -> List[T]:
    """Return the first *limit* merged items without consuming more."""
    if limit < 0:
        raise ValueError("limit must not be negative")
    result: List[T] = []
    for item in merge_sorted(streams):
        result.append(item)
        if len(result) >= limit:
            break
    return result


__all__ = ["merge_sorted", "merge_sorted_keyed", "take_head"]
