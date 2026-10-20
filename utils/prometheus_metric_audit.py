"""Prometheus metric naming lint.

Names must stay snake_case and unit suffixes make dashboards readable;
this lint flags names that break the conventions.
"""
import logging
import re

LOG = logging.getLogger(__name__)
NAME_RE = re.compile(r'^[a-z][a-z0-9_]*$')


def invalid_names(metric_names):
    """Return names that are not lower snake_case."""
    bad = [n for n in metric_names or [] if not NAME_RE.match(str(n))]
    LOG.debug('invalid metric names %d', len(bad))
    return bad


def missing_unit_suffix(metric_names, units=('seconds', 'bytes', 'total')):
    """Return measurement-looking names lacking a unit suffix."""
    missing = []
    for name in metric_names or []:
        if name.endswith('_count') or name.endswith('_bucket'):
            continue
        if any(k in name for k in ('duration', 'size', 'latency')):
            if not name.endswith(units):
                missing.append(name)
    return missing


__all__ = ['invalid_names', 'missing_unit_suffix']
