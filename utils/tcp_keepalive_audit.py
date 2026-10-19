"""TCP keepalive parameter audit.

Defaults keep dead connections for hours; the audit checks the configured
trio against the policy bounds.
"""
import logging

LOG = logging.getLogger(__name__)


def max_idle_seconds(time_sec, interval_sec, probes):
    """Return the worst case seconds before a dead peer is detected."""
    return int(time_sec) + int(interval_sec) * int(probes)


def violates(time_sec, interval_sec, probes, budget_sec=600):
    """Report when detection can take longer than the budget."""
    total = max_idle_seconds(time_sec, interval_sec, probes)
    LOG.debug('keepalive worst case %ds', total)
    return total > int(budget_sec)


__all__ = ['max_idle_seconds', 'violates']
