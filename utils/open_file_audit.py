"""Open file descriptor census.

Leaked descriptors accumulate in long-lived processes, so per-process counts
are ranked and flagged against a soft cap.
"""
import logging

LOG = logging.getLogger(__name__)


def top_consumers(fd_counts, limit=5):
    """Return the (pid, count) pairs with the most open files."""
    pairs = sorted(((int(c or 0), p) for p, c in (fd_counts or {}).items()), reverse=True)
    return [(pid, cnt) for cnt, pid in pairs[:limit]]


def over_soft_cap(fd_counts, cap=4096):
    """Return pids whose descriptor count crossed the soft cap."""
    over = [p for p, c in (fd_counts or {}).items() if int(c or 0) > cap]
    if over:
        LOG.warning('pids over fd cap: %s', over)
    return sorted(over)


__all__ = ['top_consumers', 'over_soft_cap']
