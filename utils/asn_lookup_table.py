"""ASN prefix lookup.

Routing tables map CIDR prefixes to AS numbers; longest-prefix matching
answers which network announces an address.
"""
import ipaddress
import logging

LOG = logging.getLogger(__name__)


def build_table(rows):
    """Return [(network, asn)] sorted most-specific first."""
    table = []
    for cidr, asn in rows or []:
        try:
            table.append((ipaddress.IPv4Network(cidr, strict=False), int(asn)))
        except ValueError:
            LOG.debug('skipping bad cidr %r', cidr)
    table.sort(key=lambda kv: kv[0].prefixlen, reverse=True)
    return table


def lookup(table, addr):
    """Return the ASN announcing addr, or None."""
    try:
        ip = ipaddress.IPv4Address(str(addr))
    except ValueError:
        return None
    for net, asn in table or []:
        if ip in net:
            return asn
    return None


__all__ = ['build_table', 'lookup']
