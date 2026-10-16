"""vCPU affinity audit for pinned guests.

Pinned vCPUs must occupy distinct physical CPUs, because two vCPUs sharing one
core introduces unpredictable steal between them.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def pinning_map(assignments):
    """Return a mapping of physical cpu to the vcpus pinned to it."""
    mapping = {}
    for vcpu, cpus in (assignments or {}).items():
        for cpu in cpus or []:
            mapping.setdefault(int(cpu), []).append(vcpu)
    return mapping


def shared_cores(assignments):
    """Return the physical cpus hosting more than one vcpu."""
    shared = {cpu: vcpus for cpu, vcpus in pinning_map(assignments).items() if len(vcpus) > 1}
    if shared:
        LOG.info('%d physical cpus are shared between vcpus', len(shared))
    return shared


def audit_verdict(assignments, expected_spread=1):
    """Judge whether cpu pinning honours the expected spread."""
    counts = Counter(len(v) for v in pinning_map(assignments).values())
    worst = max(counts) if counts else 0
    return 'ok' if worst <= expected_spread else 'oversubscribed'


__all__ = ['pinning_map', 'shared_cores', 'audit_verdict']
