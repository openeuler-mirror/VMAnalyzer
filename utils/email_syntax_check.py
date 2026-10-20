"""Validate e-mail address syntax with a pragmatic regular expression."""
import re

__all__ = ["is_valid_email", "split_email", "normalize_email"]

_EMAIL = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")


def is_valid_email(address):
    """Return True when *address* looks like a plain e-mail address."""
    text = str(address).strip()
    return bool(_EMAIL.match(text)) and ".." not in text


def split_email(address):
    """Split *address* into its local and domain parts."""
    local, _, domain = str(address).strip().partition("@")
    return local, domain


def normalize_email(address):
    """Lower-case the domain part and strip surrounding whitespace."""
    local, domain = split_email(address)
    return "%s@%s" % (local, domain.lower())
