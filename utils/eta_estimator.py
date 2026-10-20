"""Exponentially smoothed ETA estimator.

A raw remaining-time estimate jumps around, so the estimator blends each new
observation into a moving value using a configurable smoothing factor.
"""
from dataclasses import dataclass, field


@dataclass
class EtaEstimator:
    """Track a smoothed estimate of remaining seconds."""

    alpha: float = 0.3
    estimate: float = field(default=None)

    def observe(self, remaining):
        """Fold a fresh remaining-seconds observation into the estimate."""
        if self.estimate is None:
            self.estimate = float(remaining)
        else:
            self.estimate = self.alpha * remaining + (1.0 - self.alpha) * self.estimate
        return self.estimate

    def settled(self):
        """Report whether any observation has been folded in yet."""
        return self.estimate is not None


__all__ = ["EtaEstimator"]
