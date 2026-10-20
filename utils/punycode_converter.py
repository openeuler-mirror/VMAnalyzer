"""Punycode label audit.

Internationalised domain names encode as xn-- labels; mixed-script labels
flag possible homograph phishing.
"""
import logging

LOG = logging.getLogger(__name__)


def is_puny(label):
    """Report whether the DNS label carries the xn-- prefix."""
    return str(label or '').lower().startswith('xn--')


def puny_labels(hostname):
    """Return the labels of the hostname that are punycode."""
    labels = [l for l in str(hostname or '').split('.') if is_puny(l)]
    if labels:
        LOG.debug('punycode labels %s', labels)
    return labels


__all__ = ['is_puny', 'puny_labels']
