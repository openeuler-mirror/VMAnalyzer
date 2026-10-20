"""Grafana dashboard hygiene audit.

Panels without descriptions or units confuse on-call engineers; this
audit lists panels missing either field.
"""
import logging

LOG = logging.getLogger(__name__)


def panels_missing_description(panels):
    """Return panel titles lacking a description."""
    return [p.get('title', '?') for p in panels or []
            if not str(p.get('description', '')).strip()]


def panels_missing_unit(panels):
    """Return panel titles whose field config sets no unit."""
    missing = []
    for panel in panels or []:
        cfg = (panel.get('fieldConfig') or {}).get('defaults') or {}
        if not cfg.get('unit'):
            missing.append(panel.get('title', '?'))
    LOG.debug('panels missing unit %d', len(missing))
    return missing


__all__ = ['panels_missing_description', 'panels_missing_unit']
