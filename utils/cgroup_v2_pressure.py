"""cgroup v2 PSI parsing.

Pressure stall information reports some/full stalls per resource; the avg10
field feeds alerting.
"""
import logging

LOG = logging.getLogger(__name__)


def parse_avg10(line):
    """Return the avg10 value from a PSI line."""
    for token in str(line or '').split():
        if token.startswith('avg10='):
            try:
                return float(token.split('=', 1)[1])
            except ValueError:
                return 0.0
    return 0.0


def stalled(some_line, ceiling=10.0):
    """Report when the some-stall avg10 crossed the ceiling."""
    avg = parse_avg10(some_line)
    bad = avg >= ceiling
    if bad:
        LOG.warning('psi some avg10 %.2f >= %s', avg, ceiling)
    return bad


__all__ = ['parse_avg10', 'stalled']
