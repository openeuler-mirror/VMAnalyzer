"""IPv6 address compression.

Full 32-hex-digit addresses are unreadable; collapsing zero runs yields
the canonical short form for configs and ACLs.
"""
import ipaddress
import logging

LOG = logging.getLogger(__name__)


def compress(addr):
    """Return the canonical compressed form, or None when invalid."""
    try:
        short = ipaddress.IPv6Address(str(addr).strip()).compressed
    except ValueError:
        LOG.debug('invalid ipv6 %r', addr)
        return None
    return short


def compress_list(addrs):
    """Return {input: compressed or None} for a batch."""
    return {a: compress(a) for a in addrs or []}


__all__ = ['compress', 'compress_list']
