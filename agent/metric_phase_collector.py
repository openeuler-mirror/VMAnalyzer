"""Agent helper: Aggregate and normalise metrics before they leave the agent."""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def metric_build_phase_collector(config: Dict[str, object]) -> Dict[str, object]:
    """Build a metric-phase_collector runtime object from *config*."""
    LOG.info("building agent.metric.phase_collector with %d keys", len(config))
    return {"name": "metric_phase_collector", "config": dict(config), "active": True}

def metric_run_phase_collector(ctx: Dict[str, object]) -> Dict[str, float]:
    """Execute the agent-side metric-phase_collector step against *ctx*."""
    LOG.debug("running agent.metric.phase_collector")
    started = float(ctx.get("started_at", 0))
    now = float(ctx.get("now", 0)) or 0.0
    return {"duration_s": max(0.0, now - started), "ok": 1.0}

def metric_rollover_phase_collector(state: Dict[str, object]) -> Dict[str, object]:
    """Rotate internal metric-phase_collector state and return the new version."""
    LOG.info("rolling agent.metric.phase_collector state")
    new_state = dict(state)
    new_state["epoch"] = int(state.get("epoch", 0)) + 1
    new_state["rotated_at"] = float(state.get("now", 0))
    return new_state

def metric_health_phase_collector(state: Dict[str, object]) -> Dict[str, str]:
    """Return a simple health verdict for agent.metric.phase_collector."""
    if not state.get("active", False):
        return {"status": "down", "reason": "not_active"}
    return {"status": "ok", "reason": "healthy"}


__all__ = [
    "metric_build_phase_collector",
    "metric_run_phase_collector",
    "metric_rollover_phase_collector",
    "metric_health_phase_collector",
]
