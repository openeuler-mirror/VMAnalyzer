"""Zombie process accounting.

Zombies pile up when a parent forgets to reap; counting them per parent pid
pinpoints the offender.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def count_by_parent(zombies):
    """Return {ppid: zombie_count} from (pid, ppid) zombie entries."""
    counts = Counter(int(ppid) for _pid, ppid in zombies or [])
    return dict(counts)


def worst_parent(zombies):
    """Return the ppid owning the most zombies, or None."""
    counts = count_by_parent(zombies)
    if not counts:
        return None
    ppid, top = max(counts.items(), key=lambda kv: kv[1])
    LOG.debug('ppid %d owns %d zombies', ppid, top)
    return ppid


__all__ = ['count_by_parent', 'worst_parent']
