"""Audit helper that validates state machine transitions.

Illegal transitions such as a virtual machine jumping from migrating straight
to deleted usually indicate an out of order event stream, so every hop is
checked against a declared transition table.
"""
import logging

LOG = logging.getLogger(__name__)


def build_table(transitions):
    """Compile an iterable of (source, target) pairs into a lookup table."""
    table = {}
    for pair in transitions or []:
        source, target = pair[0], pair[1]
        table.setdefault(source, set()).add(target)
    return table


def is_legal(table, source, target):
    """Report whether the pair is a declared transition."""
    return target in table.get(source, set())


def audit_sequence(table, sequence, initial=None):
    """Return the first illegal hop as (index, source, target), or None."""
    items = list(sequence or [])
    if initial is not None:
        cursor = initial
        start = 0
    elif items:
        cursor = items[0]
        start = 1
    else:
        return None
    for index in range(start, len(items)):
        target = items[index]
        if not is_legal(table, cursor, target):
            LOG.debug('illegal transition at %d: %s -> %s', index, cursor, target)
            return index, cursor, target
        cursor = target
    return None


__all__ = ['build_table', 'is_legal', 'audit_sequence']
