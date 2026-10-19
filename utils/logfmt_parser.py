"""logfmt key extraction.

Heroku-style logfmt lines carry key=value pairs; quoted values with spaces
need a small state machine rather than a split.
"""
import logging
import re

LOG = logging.getLogger(__name__)

PAIR_RE = re.compile(r'(\w+)=(?:"([^"]*)"|(\S*))')


def parse_line(line):
    """Return the key/value dict for one logfmt line."""
    out = {}
    for key, quoted, bare in PAIR_RE.findall(str(line or '')):
        out[key] = quoted if quoted != '' else bare
    return out


def error_lines(lines):
    """Return parsed lines whose level key marks an error."""
    errs = [parse_line(l) for l in lines or []]
    errs = [p for p in errs if str(p.get('level', '')).lower() in ('error', 'err', 'crit')]
    LOG.debug('logfmt error lines %d', len(errs))
    return errs


__all__ = ['parse_line', 'error_lines']
