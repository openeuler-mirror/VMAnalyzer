"""TCP round trip time estimation helpers.

RTT samples vary wildly on loaded links; a smoothed estimator keeps the value
stable without ignoring genuine shifts.
"""
import logging

LOG = logging.getLogger(__name__)


def smooth_rtt(previous, sample, alpha=0.125):
    """Return the RFC 6298 style smoothed RTT estimate."""
    if previous is None:
        return round(float(sample), 3)
    value = (1.0 - alpha) * float(previous) + alpha * float(sample)
    return round(value, 3)


def retransmit_timeout(smoothed, deviation):
    """Return RTO = smoothed + 4 * deviation, floored at 1ms."""
    rto = float(smoothed) + 4.0 * float(deviation)
    LOG.debug('rto %.3f', rto)
    return round(max(0.001, rto), 3)


__all__ = ['smooth_rtt', 'retransmit_timeout']
