"""kptr_restrict policy audit.

Perf and tracing leak kernel pointers when kptr_restrict is zero; the sysctl
value is graded.
"""
import logging

LOG = logging.getLogger(__name__)


def grade(value):
    """Return strict, relaxed or open for the sysctl value."""
    v = int(value if value is not None else -1)
    if v >= 2:
        return 'strict'
    if v == 1:
        return 'relaxed'
    if v == 0:
        return 'open'
    return 'unknown'


def compliant(value, minimum='relaxed'):
    """Report whether the value meets the minimum grade."""
    order = {'open': 0, 'relaxed': 1, 'strict': 2}
    ok = order.get(grade(value), -1) >= order.get(minimum, 1)
    LOG.debug('kptr_restrict %s compliant=%s', value, ok)
    return ok


__all__ = ['grade', 'compliant']
