"""Kafka partition assignment balance check.

Leaders spread unevenly after broker restarts; measuring per-broker skew
shows whether a preferred-leader election would help.
"""
import logging

LOG = logging.getLogger(__name__)


def broker_loads(assignments):
    """Return {broker: leader partition count} from [(broker, partition)]."""
    loads = {}
    for broker, _part in assignments or []:
        loads[broker] = loads.get(broker, 0) + 1
    return loads


def skew_percent(assignments):
    """Return (max_load - ideal) / ideal * 100 for the hottest broker."""
    loads = broker_loads(assignments)
    if not loads:
        return 0.0
    ideal = sum(loads.values()) / float(len(loads))
    hottest = max(loads.values())
    skew = 0.0 if ideal == 0 else (hottest - ideal) / ideal * 100.0
    LOG.debug('partition skew %.2f%% hottest=%d ideal=%.2f', skew, hottest, ideal)
    return round(skew, 2)


__all__ = ['broker_loads', 'skew_percent']
