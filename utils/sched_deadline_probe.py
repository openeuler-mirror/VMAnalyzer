"""Deadline task admission.

Admission control sums runtime/period across deadline tasks; a new task fits
only under the CPU count.
"""
import logging

LOG = logging.getLogger(__name__)


def utilisation(tasks):
    """Return the summed runtime/period utilisation."""
    total = 0.0
    for t in tasks or []:
        runtime = float((t or {}).get('runtime', 0))
        period = float((t or {}).get('period', 0))
        if period > 0:
            total += runtime / period
    return round(total, 3)


def admits(tasks, new_runtime, new_period, cpus):
    """Report whether the new deadline task passes admission."""
    current = utilisation(tasks)
    extra = float(new_runtime or 0) / float(new_period or 1)
    ok = current + extra <= float(cpus or 1)
    LOG.debug('dl admit=%s (%.3f + %.3f <= %s)', ok, current, extra, cpus)
    return ok


__all__ = ['utilisation', 'admits']
