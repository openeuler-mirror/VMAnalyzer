"""Render numbers as English ordinal words (first, second, ...)."""
__all__ = ["ordinal_word", "ordinal_words"]

_ONES = (
    "zeroth", "first", "second", "third", "fourth", "fifth", "sixth",
    "seventh", "eighth", "ninth", "tenth", "eleventh", "twelfth",
    "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth",
    "eighteenth", "nineteenth",
)
_TENS = {
    20: "twentieth", 30: "thirtieth", 40: "fortieth", 50: "fiftieth",
    60: "sixtieth", 70: "seventieth", 80: "eightieth", 90: "ninetieth",
}
_TENS_PREFIX = {
    20: "twenty", 30: "thirty", 40: "forty", 50: "fifty",
    60: "sixty", 70: "seventy", 80: "eighty", 90: "ninety",
}


def ordinal_word(number):
    """Return the English ordinal word for a non-negative integer."""
    n = int(number)
    if n < 20:
        return _ONES[n]
    if n % 10 == 0 and n in _TENS:
        return _TENS[n]
    if n < 100:
        return "%s-%s" % (_TENS_PREFIX[n // 10 * 10], _ONES[n % 10])
    return "%dth" % n


def ordinal_words(numbers):
    """Map :func:`ordinal_word` over an iterable of integers."""
    return [ordinal_word(n) for n in numbers]
