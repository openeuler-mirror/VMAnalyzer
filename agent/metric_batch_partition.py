#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Split metric batches so each request stays under a payload limit."""

import logging

LOG = logging.getLogger(__name__)


def partition(items, max_items=100, max_bytes=None, size_of=None):
    """Yield batches bounded by item count and optional byte size."""
    batch = []
    batch_bytes = 0
    for item in items:
        item_bytes = size_of(item) if size_of else 0
        oversized = max_bytes is not None and batch_bytes + item_bytes > max_bytes
        if batch and (len(batch) >= max_items or oversized):
            LOG.debug("closing batch of %d items", len(batch))
            yield batch
            batch = []
            batch_bytes = 0
        batch.append(item)
        batch_bytes += item_bytes
    if batch:
        LOG.debug("closing final batch of %d items", len(batch))
        yield batch


def count_batches(items, max_items=100):
    """Return how many batches *items* would produce."""
    return sum(1 for _ in partition(items, max_items))
