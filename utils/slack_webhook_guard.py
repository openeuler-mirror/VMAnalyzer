"""Slack webhook URL guard.

Webhook URLs embed a secret path; validating hosts and redacting the
secret keeps logs and configs leak-free.
"""
import logging

LOG = logging.getLogger(__name__)


def is_valid_webhook(url, allowed_hosts=('hooks.slack.com',)):
    """Return True when the URL host is an allowed webhook host."""
    parts = str(url).split('/')
    host = parts[2] if len(parts) > 2 else ''
    return host in allowed_hosts


def redact(url):
    """Return the URL with everything past the host replaced."""
    parts = str(url).split('/')
    if len(parts) <= 3:
        return '***'
    safe = '/'.join(parts[:3]) + '/***'
    LOG.debug('redacted webhook %s', safe)
    return safe


__all__ = ['is_valid_webhook', 'redact']
