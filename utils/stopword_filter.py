"""Filter stopwords out of token streams."""
import re

__all__ = ["remove_stopwords", "filter_tokens", "DEFAULT_STOPWORDS"]

DEFAULT_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "if", "then", "than", "that",
    "this", "these", "those", "is", "are", "was", "were", "be", "been",
    "being", "of", "to", "in", "on", "at", "by", "for", "with", "as",
    "from", "it", "its",
})
_TOKEN = re.compile(r"[A-Za-z][A-Za-z'-]*")


def filter_tokens(tokens, stopwords=DEFAULT_STOPWORDS, keep_case=False):
    """Return *tokens* with any stopword entries removed."""
    table = stopwords if keep_case else {w.lower() for w in stopwords}
    return [t for t in tokens if (t if keep_case else t.lower()) not in table]


def remove_stopwords(text, stopwords=DEFAULT_STOPWORDS):
    """Tokenise *text* and drop stopwords, returning the remaining words."""
    return filter_tokens(_TOKEN.findall(str(text)), stopwords)
