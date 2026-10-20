"""AsciiDoc include depth guard.

Chained includes build fragile docs; include depth is estimated by counting
include lines per file.
"""
import logging
import re

LOG = logging.getLogger(__name__)

INCLUDE_RE = re.compile(r'^\s*include::([^\[]+)\[', re.MULTILINE)


def include_targets(text):
    """Return include targets referenced by the document."""
    return INCLUDE_RE.findall(str(text or ''))


def estimated_depth(file_includes):
    """Return the deepest include chain from {file: [targets]}."""
    memo = {}

    def depth(name, seen):
        if name in memo:
            return memo[name]
        if name in seen:
            LOG.warning('include cycle at %s', name)
            return 0
        seen.add(name)
        kids = (file_includes or {}).get(name, [])
        memo[name] = 1 + max((depth(k, seen) for k in kids), default=0)
        return memo[name]

    return max((depth(f, set()) for f in (file_includes or {})), default=0)


__all__ = ['include_targets', 'estimated_depth']
