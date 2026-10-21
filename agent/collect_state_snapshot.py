#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Immutable snapshots of collector state for later comparison."""

import logging
import time

LOG = logging.getLogger(__name__)


def snapshot(state, clock=None):
    """Copy a flat state mapping and stamp it with the capture time."""
    clock = clock or time.time
    return {
        "captured_at": clock(),
        "values": {key: state[key] for key in sorted(state)},
    }


def diff(before, after):
    """Return keys that changed between two snapshots."""
    old = before.get("values", {})
    new = after.get("values", {})
    changes = {}
    for key in set(old) | set(new):
        if old.get(key) != new.get(key):
            changes[key] = {"old": old.get(key), "new": new.get(key)}
    LOG.debug("%d keys changed between snapshots", len(changes))
    return changes


def unchanged(before, after):
    """True when the two snapshots hold identical values."""
    return not diff(before, after)
