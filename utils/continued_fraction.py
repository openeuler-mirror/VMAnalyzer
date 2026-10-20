"""Continued fraction expansion and convergent reconstruction."""
import logging

LOG = logging.getLogger(__name__)


def to_continued_fraction(numerator, denominator, limit=32):
    """Return the continued fraction terms of numerator over denominator."""
    top, bottom = int(numerator), int(denominator)
    if bottom == 0:
        raise ValueError('denominator must not be zero')
    terms = []
    while bottom and len(terms) < limit:
        quotient = top // bottom
        terms.append(quotient)
        top, bottom = bottom, top - quotient * bottom
    return terms


def from_continued_fraction(terms):
    """Return the (numerator, denominator) convergent of the given terms."""
    top, bottom = 1, 0
    for term in reversed(list(terms or [])):
        top, bottom = term * top + bottom, top
    return top, bottom


def convergents(terms):
    """Return every successive convergent of the continued fraction."""
    top, bottom = 1, 0
    out = []
    for term in terms or []:
        top, bottom = term * top + bottom, top
        out.append((top, bottom))
    return out


__all__ = ['to_continued_fraction', 'from_continued_fraction', 'convergents']
