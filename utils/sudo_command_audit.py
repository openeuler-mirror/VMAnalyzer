"""Sudo command risk classification.

Interactive shells via sudo bypass per-command logging, so commands are
classed by risk tier.
"""
import logging

LOG = logging.getLogger(__name__)

SHELLS = {'/bin/bash', '/bin/sh', '/bin/zsh', '/bin/dash'}
EDITORS = {'/usr/bin/vim', '/usr/bin/nano', '/bin/vi'}


def risk_tier(command):
    """Return high, medium or low for the sudoed command."""
    cmd = str(command or '').strip()
    if cmd.split(' ')[0] in SHELLS:
        return 'high'
    if cmd.split(' ')[0] in EDITORS:
        return 'medium'
    return 'low'


def tier_counts(commands):
    """Return {tier: count} for the command list."""
    from collections import Counter
    counts = Counter(risk_tier(c) for c in commands or [])
    LOG.debug('sudo tiers %s', dict(counts))
    return dict(counts)


__all__ = ['risk_tier', 'tier_counts']
