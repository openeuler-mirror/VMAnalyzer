"""Agent helper: Handle one specialised aspect of telemetry collection inside the agent pipeline."""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def collect_build_heartbeat_probe(config: Dict[str, object]) -> Dict[str, object]:
    """Build a collect-heartbeat_probe runtime object from *config*."""
    LOG.info("building agent.collect.heartbeat_probe with %d keys", len(config))
    return {"name": "collect_heartbeat_probe", "config": dict(config), "active": True}

def collect_run_heartbeat_probe(ctx: Dict[str, object]) -> Dict[str, float]:
    """Execute the agent-side collect-heartbeat_probe step against *ctx*."""
    LOG.debug("running agent.collect.heartbeat_probe")
    started = float(ctx.get("started_at", 0))
    now = float(ctx.get("now", 0)) or 0.0
    return {"duration_s": max(0.0, now - started), "ok": 1.0}

def collect_rollover_heartbeat_probe(state: Dict[str, object]) -> Dict[str, object]:
    """Rotate internal collect-heartbeat_probe state and return the new version."""
    LOG.info("rolling agent.collect.heartbeat_probe state")
    new_state = dict(state)
    new_state["epoch"] = int(state.get("epoch", 0)) + 1
    new_state["rotated_at"] = float(state.get("now", 0))
    return new_state

def collect_health_heartbeat_probe(state: Dict[str, object]) -> Dict[str, str]:
    """Return a simple health verdict for agent.collect.heartbeat_probe."""
    if not state.get("active", False):
        return {"status": "down", "reason": "not_active"}
    return {"status": "ok", "reason": "healthy"}


__all__ = [
    "collect_build_heartbeat_probe",
    "collect_run_heartbeat_probe",
    "collect_rollover_heartbeat_probe",
    "collect_health_heartbeat_probe",
]
