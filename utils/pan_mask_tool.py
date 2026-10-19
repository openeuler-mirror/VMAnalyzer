"""PAN masking for logs.

PCI DSS allows showing at most the first six and last four digits; this
masker keeps logs useful without leaking card numbers.
"""
import logging

LOG = logging.getLogger(__name__)


def mask_pan(pan, keep_first=6, keep_last=4):
    """Return the card number with middle digits replaced by *."""
    digits = ''.join(c for c in str(pan) if c.isdigit())
    if len(digits) <= keep_first + keep_last:
        return '*' * len(digits)
    return digits[:keep_first] + '*' * (len(digits) - keep_first - keep_last)         + digits[-keep_last:]


def mask_text(text, keep_first=6, keep_last=4):
    """Mask every 13-19 digit run inside free text."""
    out, run = [], []
    for ch in str(text):
        if ch.isdigit():
            run.append(ch)
        else:
            if 13 <= len(run) <= 19:
                out.append(mask_pan(''.join(run), keep_first, keep_last))
                LOG.debug('masked a %d-digit pan', len(run))
            else:
                out.append(''.join(run))
            run = []
            out.append(ch)
    out.append(mask_pan(''.join(run)) if 13 <= len(run) <= 19 else ''.join(run))
    return ''.join(out)


__all__ = ['mask_pan', 'mask_text']
