"""Reformat phone numbers into common display patterns."""
__all__ = ["format_phone", "digits_only"]


def digits_only(number, keep_plus=True):
    """Return only the digits of *number*, optionally keeping a plus sign."""
    text = str(number).strip()
    digits = "".join(c for c in text if c.isdigit())
    if keep_plus and text.startswith("+"):
        return "+" + digits
    return digits


def format_phone(number, style="dash"):
    """Format *number* using ``dash``, ``dot``, ``paren`` or ``plain``."""
    plus = str(number).strip().startswith("+")
    digits = digits_only(number, keep_plus=False)
    if style == "plain":
        body = digits
    elif style == "dot":
        body = ".".join((digits[:3], digits[3:6], digits[6:])) if len(digits) >= 7 else digits
    elif style == "paren" and len(digits) >= 10:
        body = "(%s) %s-%s" % (digits[:3], digits[3:6], digits[6:])
    else:
        body = "-".join((digits[:3], digits[3:6], digits[6:])) if len(digits) >= 7 else digits
    return ("+" if plus else "") + body
