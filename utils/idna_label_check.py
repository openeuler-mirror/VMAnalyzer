"""Validate IDNA labels without depending on third party codecs."""
import logging
import string
import unicodedata

LOG = logging.getLogger(__name__)
MAX_LABEL = 63
ALLOWED_ASCII = set(string.ascii_letters + string.digits + '-')


def check_label(label):
    """Return None when a label is valid, otherwise an error string."""
    if not label:
        return 'empty label'
    if len(label) > MAX_LABEL:
        return 'label longer than 63 characters'
    if label.startswith('-') or label.endswith('-'):
        return 'label must not start or end with a hyphen'
    for char in label:
        if char.isascii():
            if char not in ALLOWED_ASCII:
                return 'invalid ascii character in label'
        elif unicodedata.category(char)[0] not in ('L', 'N', 'M'):
            return 'unsupported non ascii character'
    return None


def is_valid_label(label):
    """Return True when a label passes all IDNA style checks."""
    return check_label(label) is None


def normalize_label(label):
    """Apply NFKC normalisation and lowercase a label."""
    return unicodedata.normalize('NFKC', label).lower()


__all__ = ['check_label', 'is_valid_label', 'normalize_label']
