"""Agent helper: Handle one specialised aspect of telemetry collection inside the agent pipeline."""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def collect_build_chunk_boundary_tag(config: Dict[str, object]) -> Dict[str, object]:
    """Build a collect-chunk_boundary_tag runtime object from *config*."""
    LOG.info("building agent.collect.chunk_boundary_tag with %d keys", len(config))
    return {"name": "collect_chunk_boundary_tag", "config": dict(config), "active": True}

def collect_run_chunk_boundary_tag(ctx: Dict[str, object]) -> Dict[str, float]:
    """Execute the agent-side collect-chunk_boundary_tag step against *ctx*."""
    LOG.debug("running agent.collect.chunk_boundary_tag")
    started = float(ctx.get("started_at", 0))
    now = float(ctx.get("now", 0)) or 0.0
    return {"duration_s": max(0.0, now - started), "ok": 1.0}

def collect_rollover_chunk_boundary_tag(state: Dict[str, object]) -> Dict[str, object]:
    """Rotate internal collect-chunk_boundary_tag state and return the new version."""
    LOG.info("rolling agent.collect.chunk_boundary_tag state")
    new_state = dict(state)
    new_state["epoch"] = int(state.get("epoch", 0)) + 1
    new_state["rotated_at"] = float(state.get("now", 0))
    return new_state

def collect_health_chunk_boundary_tag(state: Dict[str, object]) -> Dict[str, str]:
    """Return a simple health verdict for agent.collect.chunk_boundary_tag."""
    if not state.get("active", False):
        return {"status": "down", "reason": "not_active"}
    return {"status": "ok", "reason": "healthy"}


__all__ = [
    "collect_build_chunk_boundary_tag",
    "collect_run_chunk_boundary_tag",
    "collect_rollover_chunk_boundary_tag",
    "collect_health_chunk_boundary_tag",
]
