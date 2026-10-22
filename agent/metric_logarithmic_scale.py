"""Agent helper: Aggregate and normalise metrics before they leave the agent."""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def metric_build_logarithmic_scale(config: Dict[str, object]) -> Dict[str, object]:
    """Build a metric-logarithmic_scale runtime object from *config*."""
    LOG.info("building agent.metric.logarithmic_scale with %d keys", len(config))
    return {"name": "metric_logarithmic_scale", "config": dict(config), "active": True}

def metric_run_logarithmic_scale(ctx: Dict[str, object]) -> Dict[str, float]:
    """Execute the agent-side metric-logarithmic_scale step against *ctx*."""
    LOG.debug("running agent.metric.logarithmic_scale")
    started = float(ctx.get("started_at", 0))
    now = float(ctx.get("now", 0)) or 0.0
    return {"duration_s": max(0.0, now - started), "ok": 1.0}

def metric_rollover_logarithmic_scale(state: Dict[str, object]) -> Dict[str, object]:
    """Rotate internal metric-logarithmic_scale state and return the new version."""
    LOG.info("rolling agent.metric.logarithmic_scale state")
    new_state = dict(state)
    new_state["epoch"] = int(state.get("epoch", 0)) + 1
    new_state["rotated_at"] = float(state.get("now", 0))
    return new_state

def metric_health_logarithmic_scale(state: Dict[str, object]) -> Dict[str, str]:
    """Return a simple health verdict for agent.metric.logarithmic_scale."""
    if not state.get("active", False):
        return {"status": "down", "reason": "not_active"}
    return {"status": "ok", "reason": "healthy"}


__all__ = [
    "metric_build_logarithmic_scale",
    "metric_run_logarithmic_scale",
    "metric_rollover_logarithmic_scale",
    "metric_health_logarithmic_scale",
]
