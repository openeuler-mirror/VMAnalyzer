#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Decide retention for metric series by age and resolution."""

import logging

LOG = logging.getLogger(__name__)

POLICIES = {
    "raw": {"max_age_days": 2, "target_seconds": 15},
    "minute": {"max_age_days": 14, "target_seconds": 60},
    "hourly": {"max_age_days": 180, "target_seconds": 3600},
}


def retention_stage(age_days):
    """Pick the coarsest stage that still fits the sample age."""
    if age_days <= POLICIES["raw"]["max_age_days"]:
        return "raw"
    if age_days <= POLICIES["minute"]["max_age_days"]:
        return "minute"
    return "hourly"


def expired(age_days):
    """True when a sample is older than every policy allows."""
    return age_days > POLICIES["hourly"]["max_age_days"]


def downsample_factor(stage):
    """Ratio between the raw resolution and the stage resolution."""
    base = POLICIES["raw"]["target_seconds"]
    return max(1, POLICIES[stage]["target_seconds"] // base)


def plan(series_age_days):
    """Describe retention actions for each series age."""
    actions = []
    for age in series_age_days:
        stage = retention_stage(age)
        actions.append(
            {
                "age_days": age,
                "stage": stage,
                "expired": expired(age),
                "factor": downsample_factor(stage),
            }
        )
    LOG.debug("built retention plan for %d series", len(actions))
    return actions
