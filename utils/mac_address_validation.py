"""Validation and canonicalisation of MAC addresses.

Devices report link layer addresses with assorted separators and case, which
breaks equality tests, so they are reduced to a single canonical form.
"""
import re
import logging

LOG = logging.getLogger(__name__)

HEX = re.compile(r'^[0-9a-f]{12}$')
LOCAL_BIT = 0x02
MULTICAST_BIT = 0x01


def normalize(text):
    """Return a lower case colon separated MAC address, or None."""
    stripped = re.sub(r'[^0-9a-fA-F]', '', str(text or ''))
    if not HEX.match(stripped.lower()):
        return None
    return ':'.join(stripped.lower()[i:i + 2] for i in range(0, 12, 2))


def is_unicast(text):
    """Report whether the address is a unicast (non multicast) address."""
    canon = normalize(text)
    if canon is None:
        return False
    first_octet = int(canon.split(':')[0], 16)
    return not (first_octet & MULTICAST_BIT)


def is_locally_administered(text):
    """Report whether the address carries the locally administered bit."""
    canon = normalize(text)
    if canon is None:
        return False
    first_octet = int(canon.split(':')[0], 16)
    return bool(first_octet & LOCAL_BIT)


__all__ = ['normalize', 'is_unicast', 'is_locally_administered']
