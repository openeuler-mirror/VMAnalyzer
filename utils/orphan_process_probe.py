"""Orphaned process detection.

Processes reparented to init after their session leader died keep running
invisibly, so long lived orphans are surfaced for review.
"""
import logging

LOG = logging.getLogger(__name__)


def find_orphans(processes):
    """Return pids whose parent pid is 1 from {pid: ppid}."""
    orphans = [pid for pid, ppid in (processes or {}).items() if int(ppid) == 1]
    return sorted(orphans)


def long_lived_orphans(processes, ages_sec, min_age_sec=86400.0):
    """Return orphan pids older than the minimum age."""
    orphans = set(find_orphans(processes))
    aged = [pid for pid in orphans if float((ages_sec or {}).get(pid, 0)) >= min_age_sec]
    LOG.debug('%d long lived orphans', len(aged))
    return sorted(aged)


__all__ = ['find_orphans', 'long_lived_orphans']
