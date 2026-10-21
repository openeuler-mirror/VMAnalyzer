"""Stagger agent heartbeats so the control plane is not flooded.

Heartbeats synchronised across thousands of hosts overload the API after a
restart.  A deterministic per-host offset spreads them uniformly while
keeping each host's cadence stable.
"""

import hashlib
import logging

LOG = logging.getLogger(__name__)


def host_offset(host_name, period):
    """Return a stable heartbeat offset within one period."""
    if period <= 0:
        raise ValueError("period must be positive")
    digest = hashlib.md5(str(host_name).encode("utf-8")).digest()
    ratio = int.from_bytes(digest[:8], "big") / float(0xFFFFFFFFFFFFFFFF)
    return round(ratio * period, 3)


def next_heartbeat(host_name, period, now):
    """Return the next aligned heartbeat time for a host."""
    offset = host_offset(host_name, period)
    base = float(now) - ((float(now) - offset) % period)
    return round(base + period, 3)


def seconds_until(host_name, period, now):
    """Return how long the host should wait before its next heartbeat."""
    due = next_heartbeat(host_name, period, now)
    return round(max(0.0, due - float(now)), 3)
