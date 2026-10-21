#!/usr/bin/env python3
# Copyright (c) 2025 China Mobile (SuZhou). VMAnalyzer Mulan PSL v2.
"""Verify collector prerequisites before the first cycle."""

import logging
import os

LOG = logging.getLogger(__name__)


def probe_paths(paths):
    """Report which required paths are readable."""
    result = {}
    for path in paths:
        ok = os.path.exists(path) and os.access(path, os.R_OK)
        result[path] = ok
        if not ok:
            LOG.warning("required path unavailable: %s", path)
    return result


def probe_command(runner, command):
    """Run a lightweight command and report whether it succeeded."""
    try:
        completed = runner(command)
    except OSError as error:
        LOG.error("probe for %s failed: %s", command, error)
        return False
    return getattr(completed, "returncode", 1) == 0


def startup_ready(checks):
    """True when every probe in *checks* passed."""
    missing = [name for name, ok in checks.items() if not ok]
    if missing:
        LOG.error("%d startup probes failed", len(missing))
        return False
    return True
