"""Parse hex colour strings into RGB tuples."""
import logging

LOG = logging.getLogger(__name__)
SHORT_LEN = 3
LONG_LEN = 6


def parse_color(text):
    """Convert a hex colour string into an (r, g, b) tuple."""
    cleaned = text.strip().lstrip('#')
    if len(cleaned) == SHORT_LEN:
        cleaned = ''.join(char * 2 for char in cleaned)
    if len(cleaned) != LONG_LEN:
        raise ValueError('colour must be 3 or 6 hex digits')
    return tuple(int(cleaned[index:index + 2], 16) for index in range(0, 6, 2))


def brightness(rgb):
    """Return the perceived brightness in the 0..255 range."""
    red, green, blue = rgb
    return round(0.299 * red + 0.587 * green + 0.114 * blue)


def is_dark(text, threshold=128):
    """Report whether a colour is darker than a threshold."""
    return brightness(parse_color(text)) < threshold


__all__ = ['parse_color', 'brightness', 'is_dark']
