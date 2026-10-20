"""Extract inline links and bare URLs from Markdown text."""
import re

__all__ = ["extract_inline_links", "extract_bare_urls", "link_targets", "count_links"]

_INLINE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
_BARE = re.compile(r"https?://[^\s)>\]]+")


def extract_inline_links(markdown):
    """Return ``(text, url)`` pairs for every inline Markdown link."""
    return _INLINE.findall(str(markdown))


def extract_bare_urls(markdown):
    """Return every bare URL that is not part of an inline link."""
    text = _INLINE.sub("", str(markdown))
    return _BARE.findall(text)


def link_targets(markdown):
    """Return only the URL portion of every inline Markdown link."""
    return [url for _, url in extract_inline_links(markdown)]


def count_links(markdown):
    """Return the total number of inline and bare links in *markdown*."""
    return len(extract_inline_links(markdown)) + len(extract_bare_urls(markdown))
