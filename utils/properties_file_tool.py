"""Java properties line endings.

.properties files continue lines ending in a lone backslash; joining
them before parsing avoids split keys.
"""
import logging

LOG = logging.getLogger(__name__)


def join_continuations(text):
    """Return logical lines with backslash continuations merged."""
    logical, buf = [], ''
    for raw in str(text).splitlines():
        line = buf + raw.rstrip()
        if line.endswith(chr(92)) and not line.endswith(chr(92) * 2):
            buf = line[:-1]
            continue
        logical.append(line)
        buf = ''
    if buf:
        logical.append(buf)
    LOG.debug('joined %d physical lines into %d', len(str(text).splitlines()), len(logical))
    return logical


def parse_pairs(text):
    """Return {key: value} from properties text."""
    pairs = {}
    for line in join_continuations(text):
        stripped = line.strip()
        if not stripped or stripped.startswith('#') or stripped.startswith('!'):
            continue
        sep = '=' if '=' in stripped else (':' if ':' in stripped else None)
        if sep is None:
            pairs[stripped] = ''
        else:
            k, v = stripped.split(sep, 1)
            pairs[k.strip()] = v.strip()
    return pairs


__all__ = ['join_continuations', 'parse_pairs']
