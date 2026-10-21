"""Spread periodic collection ticks to avoid synchronised bursts.

Every agent started at boot fires its timer at the same instant, which
creates a cluster-wide spike.  Applying a per-VM deterministic jitter keeps
the average interval unchanged while smoothing the load profile.
"""

import hashlib
import logging

LOG = logging.getLogger(__name__)

MAX_JITTER_RATIO = 0.1


def stable_offset(vm_name, interval):
    """Return a deterministic offset within the allowed jitter window."""
    if interval <= 0:
        raise ValueError("interval must be positive")
    digest = hashlib.sha1(str(vm_name).encode("utf-8")).digest()
    fraction = int.from_bytes(digest[:4], "big") / float(0xFFFFFFFF)
    return round(fraction * interval * MAX_JITTER_RATIO, 4)


def next_due(vm_name, interval, last_run):
    """Return the next due timestamp with jitter applied."""
    jitter = stable_offset(vm_name, interval)
    due = float(last_run) + float(interval) + jitter
    LOG.debug("next collection for %s at %.3f (jitter %.3f)", vm_name, due, jitter)
    return due


def is_due(vm_name, interval, last_run, now):
    """Return True when the jittered schedule allows a run."""
    return float(now) >= next_due(vm_name, interval, last_run)
