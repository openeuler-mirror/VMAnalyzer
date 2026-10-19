"""NATS subject token rules.

Tokens are dot-separated and wildcards must occupy a whole token; this
probe validates subjects before publishers deploy.
"""
import logging

LOG = logging.getLogger(__name__)


def tokens_of(subject):
    """Return the dot-split non-empty tokens."""
    return [t for t in str(subject).split('.') if t]


def is_valid_subject(subject, allow_wildcards=False):
    """Return True when tokens are clean and wildcards are standalone."""
    tokens = str(subject).split('.')
    if not tokens or '' in tokens:
        return False
    for token in tokens:
        if token in ('*', '>'):
            if not allow_wildcards:
                return False
        elif '*' in token or '>' in token:
            LOG.debug('partial wildcard token %r', token)
            return False
    if '>' in tokens and tokens[-1] != '>':
        return False
    return True


__all__ = ['tokens_of', 'is_valid_subject']
