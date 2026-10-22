"""Agent helper: Aggregate and normalise metrics before they leave the agent."""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def metric_build_exponential_decay(config: Dict[str, object]) -> Dict[str, object]:
    """Build a metric-exponential_decay runtime object from *config*."""
    LOG.info("building agent.metric.exponential_decay with %d keys", len(config))
    return {"name": "metric_exponential_decay", "config": dict(config), "active": True}

def metric_run_exponential_decay(ctx: Dict[str, object]) -> Dict[str, float]:
    """Execute the agent-side metric-exponential_decay step against *ctx*."""
    LOG.debug("running agent.metric.exponential_decay")
    started = float(ctx.get("started_at", 0))
    now = float(ctx.get("now", 0)) or 0.0
    return {"duration_s": max(0.0, now - started), "ok": 1.0}

def metric_rollover_exponential_decay(state: Dict[str, object]) -> Dict[str, object]:
    """Rotate internal metric-exponential_decay state and return the new version."""
    LOG.info("rolling agent.metric.exponential_decay state")
    new_state = dict(state)
    new_state["epoch"] = int(state.get("epoch", 0)) + 1
    new_state["rotated_at"] = float(state.get("now", 0))
    return new_state

def metric_health_exponential_decay(state: Dict[str, object]) -> Dict[str, str]:
    """Return a simple health verdict for agent.metric.exponential_decay."""
    if not state.get("active", False):
        return {"status": "down", "reason": "not_active"}
    return {"status": "ok", "reason": "healthy"}


__all__ = [
    "metric_build_exponential_decay",
    "metric_run_exponential_decay",
    "metric_rollover_exponential_decay",
    "metric_health_exponential_decay",
]
