"""MQTT topic name audit.

Publishers must not use wildcards and subscribers should keep topics
short; auditing names catches misbehaving clients early.
"""
import logging

LOG = logging.getLogger(__name__)


def is_publishable(topic):
    """Return True when the topic has no wildcards and is non-empty."""
    topic = str(topic)
    ok = bool(topic) and '+' not in topic and '#' not in topic
    if not ok:
        LOG.debug('unpublishable topic %r', topic)
    return ok


def depth_of(topic):
    """Return the number of topic levels."""
    return len([t for t in str(topic).split('/') if t != ''])


def is_subscription_valid(filter_name):
    """Return True when # only appears as the final level."""
    levels = str(filter_name).split('/')
    return all(lv != '#' for lv in levels[:-1]) and '' not in levels[:-1]


__all__ = ['is_publishable', 'depth_of', 'is_subscription_valid']
