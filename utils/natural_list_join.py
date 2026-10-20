"""Join lists of items into human-friendly English sentences."""
__all__ = ["join_natural", "join_semicolon"]


def join_natural(items, conjunction="and", oxford=True):
    """Join *items* with commas and a final *conjunction*."""
    values = [str(i) for i in items]
    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return "%s %s %s" % (values[0], conjunction, values[1])
    head = ", ".join(values[:-1])
    if oxford:
        head += ","
    return "%s %s %s" % (head, conjunction, values[-1])


def join_semicolon(items):
    """Join *items* with a semicolon separator."""
    return "; ".join(str(i) for i in items)
