"""vCPU run queue depth sampling.

A sustained queue depth above the vCPU count means guests are waiting on host
CPU, so the per sample depth is aggregated into a pressure score.
"""
import logging

LOG = logging.getLogger(__name__)


def pressure_score(depths, vcpus):
    """Return the share of samples where depth exceeded the vCPU count."""
    clean = [int(d) for d in depths or [] if d is not None]
    if not clean or vcpus <= 0:
        return 0.0
    over = sum(1 for d in clean if d > vcpus)
    return round(over / float(len(clean)), 3)


def mean_depth(depths):
    """Return the average run queue depth across samples."""
    clean = [int(d) for d in depths or [] if d is not None]
    if not clean:
        return 0.0
    return round(sum(clean) / float(len(clean)), 3)


def verdict(score, busy=0.5):
    """Classify queue pressure as ok or busy."""
    return 'busy' if score >= busy else 'ok'


__all__ = ['pressure_score', 'mean_depth', 'verdict']
