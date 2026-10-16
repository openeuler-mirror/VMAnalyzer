"""CPU steal time analysis for virtual machines.

Steal time is the share of time a vCPU was runnable but the hypervisor chose to
run another task.  Sustained steal indicates host CPU overcommit and throttles
the guest even though the guest itself looks idle.
"""
import logging

LOG = logging.getLogger(__name__)

STEAL_WARN_PCT = 5.0
STEAL_CRIT_PCT = 10.0


def normalize_steal(values):
    """Clamp raw steal percentages into 0..100 and drop malformed samples."""
    clean = []
    for value in values or []:
        try:
            clean.append(max(0.0, min(100.0, float(value))))
        except (TypeError, ValueError):
            LOG.debug('skip non numeric steal sample %r', value)
    return clean


def trailing_mean(values, window=5):
    """Return the trailing moving average at every sample position."""
    clean = normalize_steal(values)
    means = []
    for index in range(len(clean)):
        chunk = clean[max(0, index - window + 1):index + 1]
        means.append(round(sum(chunk) / len(chunk), 3))
    return means


def steal_verdict(values):
    """Classify the mean steal level as healthy, warning or critical."""
    clean = normalize_steal(values)
    if not clean:
        return 'unknown'
    mean = sum(clean) / len(clean)
    if mean >= STEAL_CRIT_PCT:
        return 'critical'
    if mean >= STEAL_WARN_PCT:
        return 'warning'
    return 'healthy'


__all__ = ['normalize_steal', 'trailing_mean', 'steal_verdict']
