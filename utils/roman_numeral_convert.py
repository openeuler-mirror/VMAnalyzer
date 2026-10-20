"""Convert between integers and Roman numerals."""
__all__ = ["to_roman", "from_roman"]

_PAIRS = (
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
    (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
)
_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def to_roman(number):
    """Return the Roman numeral string for an integer in 1..3999."""
    n = int(number)
    if not 0 < n < 4000:
        raise ValueError("number out of Roman range: %r" % (number,))
    out = []
    for value, symbol in _PAIRS:
        while n >= value:
            out.append(symbol)
            n -= value
    return "".join(out)


def from_roman(text):
    """Parse a Roman numeral string back into an integer."""
    total = 0
    prev = 0
    for ch in reversed(str(text).upper()):
        value = _VALUES[ch]
        total += value if value >= prev else -value
        prev = value
    return total
