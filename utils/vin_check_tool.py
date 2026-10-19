"""VIN check digit validation.

Vehicle identification numbers weight transliterated letters; position 9
must equal the weighted sum mod 11.
"""
import logging

LOG = logging.getLogger(__name__)
VALUES = dict('0123456789X')
LETTERS = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
           'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'P': 7, 'R': 9, 'S': 2,
           'T': 3, 'U': 4, 'V': 5, 'W': 6, 'X': 7, 'Y': 8, 'Z': 9}
WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]


def _value(ch):
    return int(ch) if ch.isdigit() else LETTERS.get(ch, 0)


def vin_valid(vin):
    """Return True when the VIN check digit matches."""
    text = str(vin).upper()
    if len(text) != 17:
        return False
    total = sum(_value(c) * w for c, w in zip(text, WEIGHTS))
    check = total % 11
    expect = 'X' if check == 10 else str(check)
    ok = text[8] == expect
    LOG.debug('vin check %s vs %s', text[8], expect)
    return ok


__all__ = ['vin_valid', 'WEIGHTS']
