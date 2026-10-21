"""Choose which block devices to collect when the list is too long.

Hosts with hundreds of disks exceed the per-cycle probe budget.  Selecting
by read/write activity keeps the most relevant devices while guaranteeing
that every disk is eventually sampled.
"""

import logging

LOG = logging.getLogger(__name__)


def rank_devices(activity, limit):
    """Return the highest activity devices up to *limit*."""
    if limit <= 0:
        raise ValueError("limit must be positive")
    ordered = sorted(activity.items(), key=lambda item: abs(float(item[1])), reverse=True)
    selected = [name for name, _ in ordered[:limit]]
    LOG.debug("selected %d of %d device(s) by activity", len(selected), len(ordered))
    return selected


def round_robin(devices, cursor, limit):
    """Return the next slice of devices for fair coverage."""
    names = sorted(devices)
    if not names:
        return [], 0
    size = max(1, min(limit, len(names)))
    start = cursor % len(names)
    selected = [names[(start + offset) % len(names)] for offset in range(size)]
    return selected, (start + size) % len(names)


def merge_selection(active, rotating, devices, limit):
    """Merge activity-based and rotating selections without duplicates."""
    chosen = []
    for name in list(active) + list(rotating):
        if name in devices and name not in chosen:
            chosen.append(name)
        if len(chosen) >= limit:
            break
    return chosen
