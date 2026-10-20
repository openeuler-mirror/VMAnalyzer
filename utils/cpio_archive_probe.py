"""CPIO newc header sanity.

Newc headers carry a magic and hex fields; a corrupt header misaligns every
following member, so fields are validated first.
"""
import logging

LOG = logging.getLogger(__name__)

NEWC_MAGIC = '070701'


def valid_magic(header_text):
    """Report whether the header starts with the newc magic."""
    return str(header_text or '')[:6] == NEWC_MAGIC


def namesize(header_text):
    """Parse the filename length field of a newc header."""
    text = str(header_text or '')
    if len(text) < 110 or not valid_magic(text):
        return 0
    try:
        size = int(text[94:102], 16)
    except ValueError:
        return 0
    LOG.debug('cpio namesize %d', size)
    return size


__all__ = ['valid_magic', 'namesize']
