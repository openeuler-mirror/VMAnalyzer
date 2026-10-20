"""AppArmor profile mode census.

Profiles in complain mode log but do not block; the census counts profiles
per mode to spot unfinished enforcement.
"""
import logging
from collections import Counter

LOG = logging.getLogger(__name__)


def mode_counts(profiles):
    """Return {mode: count} from {profile: mode}."""
    counts = Counter(str(m or '').lower() for m in (profiles or {}).values())
    LOG.debug('apparmor modes %s', dict(counts))
    return dict(counts)


def complain_profiles(profiles):
    """Return profile names still in complain mode."""
    return sorted(p for p, m in (profiles or {}).items()
                  if str(m or '').lower() == 'complain')


__all__ = ['mode_counts', 'complain_profiles']
