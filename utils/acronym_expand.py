"""Expand or construct acronyms for phrases and identifiers."""
__all__ = ["make_acronym", "expand_acronym", "acronym_table", "is_known_acronym"]

ACRONYMS = {
    "HTTP": "Hypertext Transfer Protocol",
    "URL": "Uniform Resource Locator",
    "JSON": "JavaScript Object Notation",
    "CPU": "Central Processing Unit",
    "HTML": "Hypertext Markup Language",
}


def make_acronym(phrase, include_stopwords=False):
    """Build an upper-case acronym from the significant words in *phrase*."""
    stop = {"of", "the", "and", "for", "to", "a"}
    words = [w for w in str(phrase).split() if include_stopwords or w.lower() not in stop]
    return "".join(w[0].upper() for w in words if w)


def expand_acronym(acronym):
    """Return the known expansion of *acronym*, or an empty string."""
    return ACRONYMS.get(str(acronym).upper(), "")


def acronym_table():
    """Return a sorted list of ``(acronym, expansion)`` pairs."""
    return sorted(ACRONYMS.items())


def is_known_acronym(token):
    """Return True when *token* is a recognised acronym."""
    return str(token).upper() in ACRONYMS
