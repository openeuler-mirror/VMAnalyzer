"""Live migration progress tracking.

A live migration moves a running guest between hosts while it keeps executing.
Tracking the dirty page convergence tells an operator whether the migration
will finish or stall indefinitely.
"""
from dataclasses import dataclass, field
import logging

LOG = logging.getLogger(__name__)


@dataclass
class MigrationState:
    """Mutable counters describing one in flight live migration."""

    total_mb: int
    transferred_mb: int = 0
    dirty_rate_mbps: float = 0.0
    link_mbps: float = 1000.0

    def progress(self):
        """Return the completion ratio of the migration in 0..1."""
        if self.total_mb <= 0:
            return 0.0
        return round(min(1.0, self.transferred_mb / float(self.total_mb)), 4)

    def converges(self):
        """Report whether the transfer rate outpaces the dirty page rate."""
        return self.link_mbps > self.dirty_rate_mbps


def migration_verdict(state):
    """Classify a migration as done, converging or stalled."""
    if state.progress() >= 1.0:
        return 'done'
    if state.converges():
        return 'converging'
    LOG.warning('migration dirty rate exceeds link capacity')
    return 'stalled'


__all__ = ['MigrationState', 'migration_verdict']
