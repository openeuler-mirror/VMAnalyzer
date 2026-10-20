"""Convert camelCase or PascalCase identifiers to snake_case."""
import re

__all__ = ["camel_to_snake", "snake_parts", "is_camel_case", "to_snake_lines"]

_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def camel_to_snake(name, upper=False):
    """Return *name* rewritten in snake_case, optionally upper-cased."""
    parts = _BOUNDARY.split(str(name))
    snake = "_".join(p.lower() for p in parts if p)
    return snake.upper() if upper else snake


def snake_parts(name):
    """Split a camelCase name into its individual word parts."""
    return [p for p in _BOUNDARY.split(str(name)) if p]


def is_camel_case(name):
    """Return True when *name* contains an upper-case letter past position 0."""
    text = str(name)
    return text[:1].islower() and any(c.isupper() for c in text[1:])


def to_snake_lines(names):
    """Convert an iterable of identifiers into snake_case strings."""
    return [camel_to_snake(n) for n in names]
