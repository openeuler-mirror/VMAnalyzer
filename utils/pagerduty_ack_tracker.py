"""PagerDuty acknowledgement tracking.

Incidents paged but not acknowledged within the SLO escalate; listing
stale unacked incidents keeps the queue honest.
"""
import logging
import time

LOG = logging.getLogger(__name__)


def stale_unacked(incidents, ack_slo_sec=300, now=None):
    """Return incidents unacked longer than the SLO."""
    now = time.time() if now is None else now
    stale = []
    for inc in incidents or []:
        if inc.get('status') != 'acknowledged':
            age = now - float(inc.get('opened_ts', now))
            if age > ack_slo_sec:
                stale.append(inc)
    LOG.debug('stale unacked incidents %d', len(stale))
    return stale


def ack_rate(incidents):
    """Return the fraction of incidents that got acknowledged."""
    total = len(incidents or [])
    if total == 0:
        return 0.0
    acked = sum(1 for i in incidents if i.get('status') == 'acknowledged')
    return round(acked / float(total), 4)


__all__ = ['stale_unacked', 'ack_rate']
