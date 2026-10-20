"""Extract initials from personal names and word sequences."""
__all__ = ["extract_initials", "format_initials", "surname_first"]


def extract_initials(name, separator=""):
    """Return the initials of each word in *name* joined by *separator*."""
    words = [w for w in str(name).replace("-", " ").split() if w]
    return separator.join(w[0].upper() for w in words)


def format_initials(name, dotted=False):
    """Format initials either dotted (``J. R. R.``) or compact (``JRR``)."""
    initials = extract_initials(name)
    if dotted and initials:
        return ". ".join(initials) + "."
    return initials


def surname_first(name):
    """Return the surname followed by the extracted given initials."""
    words = [w for w in str(name).split() if w]
    if len(words) < 2:
        return str(name)
    given = extract_initials(" ".join(words[:-1]), separator=" ")
    return "%s, %s" % (words[-1], given)
