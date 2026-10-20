"""IBAN mod-97 validation.

IBANs embed a two-digit checksum validated by mod-97 arithmetic after
moving the country prefix to the end.
"""
import logging

LOG = logging.getLogger(__name__)


def _to_numeric(iban):
    out = []
    for ch in iban:
        out.append(str(ord(ch) - 55) if ch.isalpha() else ch)
    return ''.join(out)


def iban_valid(iban):
    """Return True when the IBAN checksum is correct."""
    text = str(iban).replace(' ', '').upper()
    if len(text) < 4 or not text[:2].isalpha():
        return False
    rearranged = _to_numeric(text[4:] + text[:4])
    remainder = 0
    for ch in rearranged:
        remainder = (remainder * 10 + int(ch)) % 97
    ok = remainder == 1
    LOG.debug('iban %s valid=%s', text[:4] + '...', ok)
    return ok


__all__ = ['iban_valid']
