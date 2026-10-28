"""Plan how pipeline timeout work is split into bounded batches.

A single collection round can queue more work than one pass should handle.
The planner slices the work list into batches that respect both a size limit
and an optional weight budget.
"""

import logging

LOG = logging.getLogger(__name__)


def chunk(items, size=50):
    """Split *items* into consecutive lists of at most *size* entries."""
    if size < 1:
        raise ValueError("batch size must be positive")
    sequence = list(items or [])
    return [sequence[start:start + size]
            for start in range(0, len(sequence), size)]


def plan_by_weight(items, weights, budget):
    """Group items so each group stays within *budget* accumulated weight."""
    batches, current, used = [], [], 0.0
    for item, weight in zip(items or [], weights or []):
        value = float(weight)
        if current and used + value > budget:
            batches.append(current)
            current, used = [], 0.0
        current.append(item)
        used += value
    if current:
        batches.append(current)
    LOG.debug("planned %d pipeline_timeout batches", len(batches))
    return batches


def estimate_rounds(total, size=50):
    """Return how many batches are needed for *total* work items."""
    if size < 1:
        raise ValueError("batch size must be positive")
    return (int(total) + size - 1) // size


__all__ = ["chunk", "plan_by_weight", "estimate_rounds"]
