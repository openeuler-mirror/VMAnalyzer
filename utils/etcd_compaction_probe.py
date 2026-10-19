"""etcd compaction lag probe.

When the compacted revision falls far behind the current revision the
store grows and range queries slow down.
"""
import logging

LOG = logging.getLogger(__name__)


def compaction_lag(current_revision, compact_revision):
    """Return how many revisions remain uncompacted."""
    lag = max(0, int(current_revision) - int(compact_revision))
    LOG.debug('etcd compaction lag %d', lag)
    return lag


def needs_compaction(current_revision, compact_revision, budget=10000):
    """Return True when the lag exceeds the revision budget."""
    return compaction_lag(current_revision, compact_revision) > budget


__all__ = ['compaction_lag', 'needs_compaction']
