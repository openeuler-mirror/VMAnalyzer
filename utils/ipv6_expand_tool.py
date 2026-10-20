"""IPv6 address expansion.

Some firewall tables want the exploded eight-group form; expanding also
makes textual prefix comparisons safe.
"""
import ipaddress
import logging

LOG = logging.getLogger(__name__)


def expand(addr):
    """Return the exploded 39-character form, or None when invalid."""
    try:
        full = ipaddress.IPv6Address(str(addr).strip()).exploded
    except ValueError:
        LOG.debug('invalid ipv6 %r', addr)
        return None
    return full


def same_network(a, b, prefix=64):
    """Return True when both addresses share the leading prefix bits."""
    try:
        na = ipaddress.IPv6Network('%s/%d' % (a, prefix), strict=False)
        return ipaddress.IPv6Address(str(b)) in na
    except ValueError:
        return False


__all__ = ['expand', 'same_network']
