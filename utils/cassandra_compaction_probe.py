"""Cassandra pending compaction triage.

Pending compaction tasks per table show which column family cannot keep
up with its write load.
"""
import logging

LOG = logging.getLogger(__name__)


def pending_by_table(rows):
    """Return {table: pending_tasks} from nodetool compactionstats rows."""
    pending = {}
    for row in rows or []:
        pending[row.get('table', 'unknown')] = int(row.get('pending', 0))
    return pending


def busiest_table(rows):
    """Return (table, pending) with the most pending tasks."""
    pending = pending_by_table(rows)
    top = max(pending.items(), key=lambda kv: kv[1], default=(None, 0))
    LOG.debug('busiest compaction table %s pending=%d', top[0], top[1])
    return top


__all__ = ['pending_by_table', 'busiest_table']
