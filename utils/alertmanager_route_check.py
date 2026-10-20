"""Alertmanager route matching.

An alert only reaches a receiver when some route matches all of its
labels; this check finds alerts that fall through to the default.
"""
import logging

LOG = logging.getLogger(__name__)


def route_matches(alert_labels, route_matchers):
    """Return True when every matcher label equals the alert label."""
    for key, want in (route_matchers or {}).items():
        if (alert_labels or {}).get(key) != want:
            return False
    return True


def first_matching_route(alert_labels, routes):
    """Return the first route name matching the alert, else default."""
    for route in routes or []:
        if route_matches(alert_labels, route.get('match', {})):
            return route.get('name', 'unnamed')
    LOG.debug('alert fell through to default route')
    return 'default'


__all__ = ['route_matches', 'first_matching_route']
