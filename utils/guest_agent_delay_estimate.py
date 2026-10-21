"""Estimate guest agent responsiveness from command round-trip samples.

Collectors need to distinguish a slow guest from an idle one.  Comparing
recent round-trip times against an EWMA baseline gives a delay factor that
adapts to each guest's normal performance.
"""

import logging
from typing import Dict, Iterable

LOG = logging.getLogger(__name__)


def ewma(samples: Iterable[float], alpha: float = 0.3) -> float:
    """Return the exponentially weighted average of round-trip samples."""
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be within (0, 1]")
    value = None
    for sample in samples:
        value = float(sample) if value is None else alpha * float(sample) + (1 - alpha) * value
    return value or 0.0


def delay_factor(latencies: Iterable[float], baseline: float) -> float:
    """Return the latest latency as a multiple of the baseline."""
    samples = [float(value) for value in latencies]
    if not samples or baseline <= 0:
        return 1.0
    return round(samples[-1] / baseline, 2)


def assess(latencies: Iterable[float]) -> Dict[str, object]:
    """Summarise latency samples into an agent health assessment."""
    samples = [float(value) for value in latencies]
    if not samples:
        return {"samples": 0, "baseline": 0.0, "latest": 0.0, "factor": 1.0, "state": "unknown"}
    baseline = ewma(samples)
    factor = delay_factor(samples, baseline)
    state = "healthy" if factor < 2.0 else ("slow" if factor < 5.0 else "stalled")
    if state != "healthy":
        LOG.warning("guest agent %s, delay factor %.2f", state, factor)
    return {"samples": len(samples), "baseline": round(baseline, 4),
            "latest": samples[-1], "factor": factor, "state": state}


__all__ = ["ewma", "delay_factor", "assess"]
