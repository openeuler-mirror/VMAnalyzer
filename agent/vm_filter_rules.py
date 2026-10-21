"""Decide which domains a collection pass should include.

Operators exclude templates, test guests and migrated-away domains.  A small
ordered rule set is easier to audit than scattered conditional statements in
the collector loop.
"""

import logging
import re

LOG = logging.getLogger(__name__)

DEFAULT_EXCLUDED_STATES = ("shut off", "crashed")


def compile_rule(pattern):
    """Compile a name pattern, raising a clear error on invalid regex."""
    try:
        return re.compile(pattern)
    except re.error as error:
        raise ValueError("invalid VM name pattern {!r}: {}".format(pattern, error))


def should_collect(vm, include=None, exclude=None,
                   excluded_states=DEFAULT_EXCLUDED_STATES):
    """Return True when a domain passes the configured filters."""
    state = str(vm.get("state", "")).strip().lower()
    if state in excluded_states:
        LOG.debug("skipping %s in state %s", vm.get("name"), state)
        return False
    name = str(vm.get("name", ""))
    if include and not any(compile_rule(pattern).search(name) for pattern in include):
        return False
    if exclude and any(compile_rule(pattern).search(name) for pattern in exclude):
        LOG.debug("name %s matched an exclusion rule", name)
        return False
    return True


def partition(vms, **options):
    """Split a domain list into selected and skipped names."""
    selected, skipped = [], []
    for vm in vms:
        if should_collect(vm, **options):
            selected.append(vm.get("name"))
        else:
            skipped.append(vm.get("name"))
    LOG.debug("selected %d of %d domain(s)", len(selected), len(selected) + len(skipped))
    return selected, skipped
