"""systemd unit state tally.

Failed units linger after boot; states are tallied and failed units listed
for the report.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def state_counts(units):
    """Return {state: count} from {unit: state}."""
    counts = Counter(str(s or '').lower() for s in (units or {}).values())
    LOG.debug('unit states %s', dict(counts))
    return dict(counts)


def failed_units(units):
    """Return unit names in failed state."""
    return sorted(u for u, s in (units or {}).items() if str(s or '').lower() == 'failed')


__all__ = ['state_counts', 'failed_units']
