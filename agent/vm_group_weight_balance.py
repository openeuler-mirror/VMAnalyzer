#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Balance VM collection work across groups."""

import logging

LOG = logging.getLogger(__name__)


def assign(vms, groups, weight_of=None):
    """Greedily place the heaviest VM into the lightest group."""
    if not groups:
        return {}
    weight_of = weight_of or (lambda vm: 1.0)
    loads = {group: 0.0 for group in groups}
    placement = {group: [] for group in groups}
    for vm in sorted(vms, key=weight_of, reverse=True):
        target = min(loads, key=loads.get)
        placement[target].append(vm)
        loads[target] += max(0.0, float(weight_of(vm)))
    LOG.debug("balanced %d vms across %d groups", len(vms), len(groups))
    return placement


def imbalance(placement):
    """Difference between the largest and smallest group."""
    sizes = [len(members) for members in placement.values()]
    if not sizes:
        return 0
    return max(sizes) - min(sizes)


def heaviest_group(placement, weight_of=None):
    """Name of the group carrying the most weight."""
    weight_of = weight_of or (lambda vm: 1.0)
    if not placement:
        return None
    return max(placement, key=lambda group: sum(weight_of(vm) for vm in placement[group]))
