"""Agent helper: Handle one specialised aspect of telemetry collection inside the agent pipeline."""

import logging
from typing import Dict

LOG = logging.getLogger(__name__)


def collect_build_stream_fragment(config: Dict[str, object]) -> Dict[str, object]:
    """Build a collect-stream_fragment runtime object from *config*."""
    LOG.info("building agent.collect.stream_fragment with %d keys", len(config))
    return {"name": "collect_stream_fragment", "config": dict(config), "active": True}

def collect_run_stream_fragment(ctx: Dict[str, object]) -> Dict[str, float]:
    """Execute the agent-side collect-stream_fragment step against *ctx*."""
    LOG.debug("running agent.collect.stream_fragment")
    started = float(ctx.get("started_at", 0))
    now = float(ctx.get("now", 0)) or 0.0
    return {"duration_s": max(0.0, now - started), "ok": 1.0}

def collect_rollover_stream_fragment(state: Dict[str, object]) -> Dict[str, object]:
    """Rotate internal collect-stream_fragment state and return the new version."""
    LOG.info("rolling agent.collect.stream_fragment state")
    new_state = dict(state)
    new_state["epoch"] = int(state.get("epoch", 0)) + 1
    new_state["rotated_at"] = float(state.get("now", 0))
    return new_state

def collect_health_stream_fragment(state: Dict[str, object]) -> Dict[str, str]:
    """Return a simple health verdict for agent.collect.stream_fragment."""
    if not state.get("active", False):
        return {"status": "down", "reason": "not_active"}
    return {"status": "ok", "reason": "healthy"}


__all__ = [
    "collect_build_stream_fragment",
    "collect_run_stream_fragment",
    "collect_rollover_stream_fragment",
    "collect_health_stream_fragment",
]
