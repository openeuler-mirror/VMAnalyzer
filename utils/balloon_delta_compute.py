"""Compute balloon target adjustments from guest memory pressure.

Ballooning too aggressively causes swap inside the guest.  This helper caps
inflation per cycle and avoids deflating below the guest's requested floor,
which keeps memory reclaim gradual.
"""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def compute_delta(current: int, target: int, max_step: int,
                  floor: int) -> int:
    """Return the clamped balloon size change to apply."""
    if max_step <= 0:
        raise ValueError("max_step must be positive")
    desired = max(target, floor)
    change = desired - current
    clamped = max(-max_step, min(max_step, change))
    LOG.debug("balloon delta from %d to %d clamped to %d", current, desired, clamped)
    return clamped


def plan(current: int, target: int, max_step: int, floor: int) -> Dict[str, int]:
    """Return the next balloon size and the applied delta."""
    delta = compute_delta(current, target, max_step, floor)
    return {"current": current, "target": target, "next": current + delta, "delta": delta}


def steps_required(current: int, target: int, max_step: int) -> int:
    """Return how many cycles are needed to reach the target."""
    if max_step <= 0:
        raise ValueError("max_step must be positive")
    remaining = abs(target - current)
    return (remaining + max_step - 1) // max_step


__all__ = ["compute_delta", "plan", "steps_required"]
