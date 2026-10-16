"""Out of memory kill risk estimation.

The kernel ranks processes with a kill score before choosing a victim, so the
agent can precompute a comparable risk estimate and warn before the kill.
"""
import logging

LOG = logging.getLogger(__name__)


def oom_score(rss_pages, total_pages, swap_pages=0):
    """Estimate a normalised out of memory score for a process."""
    if int(total_pages) <= 0:
        LOG.debug('total pages must be positive')
        return 0
    used = max(0, int(rss_pages) + int(swap_pages))
    return min(1000, 1000 * used // int(total_pages))


def predict_kill_order(processes, total_pages):
    """Return process names ordered from most to least kill likely."""
    scored = [(p.get('name'), oom_score(p.get('rss_pages', 0), total_pages,
                                        p.get('swap_pages', 0)))
              for p in processes or []]
    return [name for name, _ in sorted(scored, key=lambda item: item[1], reverse=True)]


def risk_verdict(score, warn=500, crit=800):
    """Classify a kill risk score as low, elevated or imminent."""
    if score >= crit:
        return 'imminent'
    if score >= warn:
        return 'elevated'
    return 'low'


__all__ = ['oom_score', 'predict_kill_order', 'risk_verdict']
