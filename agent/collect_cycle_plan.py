#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Build a weighted collection plan across VMs."""

import logging

LOG = logging.getLogger(__name__)


def plan_cycle(vms, budget, weight_of=None):
    """Allocate a per-VM share of *budget* proportional to weight."""
    if weight_of is None:
        weight_of = lambda vm: 1.0
    weighted = [(vm, max(0.01, float(weight_of(vm)))) for vm in vms]
    total = sum(weight for _, weight in weighted)
    if total <= 0:
        LOG.debug("no weights available, skipping plan")
        return []
    plan = []
    for vm, weight in weighted:
        plan.append((vm, round(budget * weight / total, 3)))
    LOG.debug("planned %d vms over budget %.3f", len(plan), budget)
    return plan


def ordered_plan(plan):
    """Sort the plan by descending share for fair scheduling."""
    return sorted(plan, key=lambda entry: entry[1], reverse=True)


def plan_total(plan):
    """Sum of the allocated shares."""
    return round(sum(share for _, share in plan), 3)
