"""Agent helper: Aggregate and normalise metrics before they leave the agent."""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def metric_build_adaptive_bucket(config: Dict[str, object]) -> Dict[str, object]:
    """Build a metric-adaptive_bucket runtime object from *config*."""
    LOG.info("building agent.metric.adaptive_bucket with %d keys", len(config))
    return {"name": "metric_adaptive_bucket", "config": dict(config), "active": True}

def metric_run_adaptive_bucket(ctx: Dict[str, object]) -> Dict[str, float]:
    """Execute the agent-side metric-adaptive_bucket step against *ctx*."""
    LOG.debug("running agent.metric.adaptive_bucket")
    started = float(ctx.get("started_at", 0))
    now = float(ctx.get("now", 0)) or 0.0
    return {"duration_s": max(0.0, now - started), "ok": 1.0}

def metric_rollover_adaptive_bucket(state: Dict[str, object]) -> Dict[str, object]:
    """Rotate internal metric-adaptive_bucket state and return the new version."""
    LOG.info("rolling agent.metric.adaptive_bucket state")
    new_state = dict(state)
    new_state["epoch"] = int(state.get("epoch", 0)) + 1
    new_state["rotated_at"] = float(state.get("now", 0))
    return new_state

def metric_health_adaptive_bucket(state: Dict[str, object]) -> Dict[str, str]:
    """Return a simple health verdict for agent.metric.adaptive_bucket."""
    if not state.get("active", False):
        return {"status": "down", "reason": "not_active"}
    return {"status": "ok", "reason": "healthy"}


__all__ = [
    "metric_build_adaptive_bucket",
    "metric_run_adaptive_bucket",
    "metric_rollover_adaptive_bucket",
    "metric_health_adaptive_bucket",
]
