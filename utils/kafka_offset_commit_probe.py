"""Kafka offset commit risk probe.

Committing on an interval means a rebalance replays everything consumed
since the last commit; estimating the replay volume sizes the blast
radius.
"""
import logging

LOG = logging.getLogger(__name__)


def replay_estimate(rate_per_sec, commit_interval_sec):
    """Return messages replayed after a worst-case rebalance."""
    replay = max(0.0, float(rate_per_sec)) * max(0.0, float(commit_interval_sec))
    LOG.debug('worst-case replay %.0f messages', replay)
    return int(replay)


def safe_interval(rate_per_sec, replay_budget=1000):
    """Return the largest commit interval keeping replay under budget."""
    if rate_per_sec <= 0:
        return float('inf')
    return round(float(replay_budget) / float(rate_per_sec), 3)


__all__ = ['replay_estimate', 'safe_interval']
