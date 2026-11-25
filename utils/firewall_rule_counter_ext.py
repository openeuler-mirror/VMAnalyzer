"""Firewall rule counting per table.

Rule count explosions slow every packet; counting rules per table shows which
subsystem is responsible.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def count_per_table(rule_lines):
    """Return {table: rule_count} parsed from iptables-save style lines."""
    counts = Counter()
    current = 'filter'
    for line in rule_lines or []:
        line = str(line).strip()
        if line.startswith('*'):
            current = line.lstrip('*')
        elif line.startswith('-A'):
            counts[current] += 1
    return dict(counts)


def largest_table(counts):
    """Return the table with the most rules, or None."""
    if not counts:
        return None
    table, top = max(counts.items(), key=lambda kv: kv[1])
    LOG.debug('table %s has %d rules', table, top)
    return table


__all__ = ['count_per_table', 'largest_table']
