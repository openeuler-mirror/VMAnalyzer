"""IMEI validation.

Device IMEIs are 15 digits ending in a Luhn check digit; validating
blocks mistyped device inventories.
"""
import logging

LOG = logging.getLogger(__name__)


def imei_valid(imei):
    """Return True when the IMEI is 15 digits and Luhn-clean."""
    text = str(imei)
    if len(text) != 15 or not text.isdigit():
        return False
    total = 0
    for i, ch in enumerate(reversed(text)):
        d = int(ch)
        if i % 2 == 1:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        total += d
    ok = total % 10 == 0
    LOG.debug('imei valid=%s', ok)
    return ok


def tac_of(imei):
    """Return the 8-digit type allocation code prefix."""
    return str(imei)[:8]


__all__ = ['imei_valid', 'tac_of']
