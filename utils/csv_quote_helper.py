"""Quote, escape and rejoin CSV field values."""
__all__ = ["needs_quoting", "quote_field", "quote_row"]


def needs_quoting(field, delimiter=",", quotechar='"'):
    """Return True when *field* must be quoted inside a CSV record."""
    text = str(field)
    return any(c in text for c in (delimiter, quotechar, "\n", "\r"))


def quote_field(field, delimiter=",", quotechar='"'):
    """Return *field* quoted and escaped for CSV output when needed."""
    text = str(field)
    if not needs_quoting(text, delimiter, quotechar):
        return text
    return quotechar + text.replace(quotechar, quotechar * 2) + quotechar


def quote_row(fields, delimiter=","):
    """Quote each field and join the row with *delimiter*."""
    return delimiter.join(quote_field(f, delimiter) for f in fields)
