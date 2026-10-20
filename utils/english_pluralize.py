"""Form English plurals with a small set of regular rules."""
__all__ = ["pluralize", "is_plural_candidate", "UNCOUNTABLE"]

_IRREGULAR = {
    "child": "children", "person": "people", "man": "men", "woman": "women",
    "tooth": "teeth", "foot": "feet", "mouse": "mice", "goose": "geese",
}
UNCOUNTABLE = frozenset({
    "sheep", "fish", "series", "species", "deer", "equipment", "information",
})


def _match_case(original, lower_form):
    """Mirror the capitalisation of *original* onto *lower_form*."""
    if original.isupper():
        return lower_form.upper()
    if original[:1].isupper():
        return lower_form.capitalize()
    return lower_form


def pluralize(word, count=2):
    """Return the plural form of *word* (or the singular when count == 1)."""
    text = str(word)
    if count == 1:
        return text
    lower = text.lower()
    if lower in UNCOUNTABLE:
        return text
    if lower in _IRREGULAR:
        return _match_case(text, _IRREGULAR[lower])
    if lower.endswith("y") and len(lower) > 1 and lower[-2] not in "aeiou":
        return text[:-1] + "ies"
    if lower.endswith(("s", "x", "z", "ch", "sh")):
        return text + "es"
    return text + "s"


def is_plural_candidate(word):
    """Return True when *word* is not an uncountable noun."""
    return str(word).lower() not in UNCOUNTABLE
