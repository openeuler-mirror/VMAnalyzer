"""AMQP exchange binding audit.

Messages published to an exchange with no matching binding vanish;
counting bindings per exchange flags the unroutable ones.
"""
import logging

LOG = logging.getLogger(__name__)


def binding_counts(bindings):
    """Return {exchange: binding count}."""
    counts = {}
    for binding in bindings or []:
        ex = binding.get('exchange', 'unknown')
        counts[ex] = counts.get(ex, 0) + 1
    return counts


def unroutable_exchanges(exchanges, bindings):
    """Return exchange names with zero bindings."""
    counts = binding_counts(bindings)
    dead = [e for e in exchanges or [] if counts.get(e, 0) == 0]
    LOG.debug('unroutable exchanges %s', dead)
    return dead


__all__ = ['binding_counts', 'unroutable_exchanges']
