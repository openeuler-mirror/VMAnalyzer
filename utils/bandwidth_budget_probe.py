"""Link bandwidth budget tracking.

Comparing achieved throughput against the provisioned budget shows how close a
guest is to saturating its share of the host uplink, which is a prerequisite for
fair scheduling decisions.
"""
import logging

LOG = logging.getLogger(__name__)


def utilisation(throughput_bps, budget_bps):
    """Return the share of the provisioned bandwidth in use."""
    budget = float(budget_bps)
    if budget <= 0:
        LOG.debug('budget is not positive')
        return 0.0
    return round(max(0.0, float(throughput_bps)) / budget, 4)


def headroom_bps(throughput_bps, budget_bps):
    """Return the still available bandwidth in bits per second."""
    return max(0.0, float(budget_bps) - float(throughput_bps))


def budget_verdict(throughput_bps, budget_bps, warn=0.8, crit=0.98):
    """Classify bandwidth pressure as normal, near limit or saturated."""
    used = utilisation(throughput_bps, budget_bps)
    if used >= crit:
        return 'saturated'
    if used >= warn:
        return 'near_limit'
    return 'normal'


__all__ = ['utilisation', 'headroom_bps', 'budget_verdict']
