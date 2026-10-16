"""Interrupt affinity audit for latency sensitive guests.

An interrupt handled on a CPU that runs the workload steals time from it, so the
spread of interrupt affinities across cpus is verified.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def target_cpus(affinity_strings):
    """Return the distinct cpus targeted by a set of affinity strings."""
    targets = set()
    for value in affinity_strings or []:
        for cpu in str(value).replace(',', ' ').split():
            if cpu.isdigit():
                targets.add(int(cpu))
    return sorted(targets)


def concentration(affinity_strings):
    """Return how concentrated the interrupt load is on one cpu."""
    counts = Counter(int(cpu) for value in affinity_strings or []
                     for cpu in str(value).replace(',', ' ').split() if cpu.isdigit())
    if not counts:
        LOG.debug('no valid affinity targets found')
        return 1.0
    return round(max(counts.values()) / float(sum(counts.values())), 4)


def spread_verdict(affinity_strings, limit=0.5):
    """Classify interrupt affinity as spread or concentrated."""
    return 'spread' if concentration(affinity_strings) <= limit else 'concentrated'


__all__ = ['target_cpus', 'concentration', 'spread_verdict']
