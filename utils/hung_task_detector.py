"""Hung task warning analysis.

Tasks stuck in D state beyond the hung task timeout point at storage or
driver trouble, so warnings are counted per command name.
"""
import logging
import re
from collections import Counter

LOG = logging.getLogger(__name__)

PATTERN = re.compile(r'task (\S+):\d+ blocked for more than (\d+) seconds')


def parse_line(line):
    """Return (command, seconds) from a hung task line, or None."""
    match = PATTERN.search(str(line or ''))
    if not match:
        return None
    return match.group(1), int(match.group(2))


def count_by_command(lines):
    """Return {command: occurrences} across log lines."""
    counts = Counter()
    for line in lines or []:
        parsed = parse_line(line)
        if parsed:
            counts[parsed[0]] += 1
    LOG.debug('hung tasks across %d commands', len(counts))
    return dict(counts)


__all__ = ['parse_line', 'count_by_command']
