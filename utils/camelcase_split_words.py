"""Split camelCase and PascalCase identifiers into readable words."""
import re

__all__ = ["split_camel_words", "humanize_camel", "abbreviate_camel", "count_camel_words"]

_BOUNDARY = re.compile(
    r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[A-Za-z])(?=[0-9])"
)


def split_camel_words(name):
    """Return the lowercase word components of a camelCase identifier."""
    return [w.lower() for w in _BOUNDARY.split(str(name)) if w]


def humanize_camel(name):
    """Turn a camelCase identifier into a capitalised, spaced phrase."""
    return " ".join(word.capitalize() for word in split_camel_words(name))


def abbreviate_camel(name):
    """Return the upper-case initials of a camelCase identifier."""
    return "".join(word[0] for word in split_camel_words(name) if word)


def count_camel_words(name):
    """Return how many word components a camelCase identifier has."""
    return len(split_camel_words(name))
