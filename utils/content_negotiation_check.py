"""HTTP content negotiation.

Accept headers carry q-values; picking the best supported type keeps
clients on representations they actually understand.
"""
import logging

LOG = logging.getLogger(__name__)


def parse_accept(header):
    """Return [(media_type, q)] sorted by preference."""
    prefs = []
    for part in str(header).split(','):
        bits = part.strip().split(';')
        q = 1.0
        for bit in bits[1:]:
            if bit.strip().startswith('q='):
                try:
                    q = float(bit.strip()[2:])
                except ValueError:
                    q = 0.0
        if bits[0]:
            prefs.append((bits[0], q))
    prefs.sort(key=lambda kv: kv[1], reverse=True)
    return prefs


def choose(header, supported):
    """Return the best supported media type, or None."""
    for media, q in parse_accept(header):
        if q <= 0:
            continue
        if media == '*/*' and supported:
            return supported[0]
        for cand in supported or []:
            if media == cand or media.endswith('/*') and                     cand.startswith(media[:-1]):
                LOG.debug('negotiated %s', cand)
                return cand
    return None


__all__ = ['parse_accept', 'choose']
