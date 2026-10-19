"""RPM header dependency skim.

RPM requires/provides lists decide install order; the requirement names are
filtered to drop rpmlib-internal entries.
"""
import logging

LOG = logging.getLogger(__name__)


def real_requires(require_names):
    """Return requirement names that are not rpmlib internal."""
    real = [n for n in require_names or [] if not str(n).startswith('rpmlib(')]
    LOG.debug('rpm real requires %d of %d', len(real), len(require_names or []))
    return real


def provides_share(provide_names, require_names):
    """Return the share of requirements satisfied by own provides."""
    reqs = set(real_requires(require_names))
    provs = {str(p) for p in provide_names or []}
    if not reqs:
        return 1.0
    return round(len(reqs & provs) / float(len(reqs)), 3)


__all__ = ['real_requires', 'provides_share']
