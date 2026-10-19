"""Kernel softlockup message parsing.

Softlockups report a stuck CPU; extracting the stuck cpu id and duration from
log lines turns them into structured counters.
"""
import logging
import re

LOG = logging.getLogger(__name__)

PATTERN = re.compile(r'soft lockup - CPU#(\d+) stuck for (\d+)s')


def parse_line(line):
    """Return (cpu, seconds) from a softlockup log line, or None."""
    match = PATTERN.search(str(line or ''))
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def summarize(lines):
    """Return {cpu: total_stuck_seconds} across many log lines."""
    totals = {}
    for line in lines or []:
        parsed = parse_line(line)
        if parsed:
            cpu, secs = parsed
            totals[cpu] = totals.get(cpu, 0) + secs
    LOG.debug('softlockup on %d cpus', len(totals))
    return totals


__all__ = ['parse_line', 'summarize']
