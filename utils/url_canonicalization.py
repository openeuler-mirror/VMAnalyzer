"""Canonicalize URLs so semantically equal addresses compare equal as strings."""

from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

DEFAULT_PORTS = {"http": 80, "https": 443}


def canonical_url(url):
    """Return a normalized URL string with a lowercase host and no default port."""
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()
    if scheme in DEFAULT_PORTS and netloc.endswith(":{}".format(DEFAULT_PORTS[scheme])):
        netloc = netloc[: -len(str(DEFAULT_PORTS[scheme])) - 1]
    query = urlencode(sorted(parse_qsl(parts.query, keep_blank_values=True)))
    path = parts.path or "/"
    return urlunsplit((scheme, netloc, path, query, ""))


def urls_equal(left, right):
    """Return True when two URLs canonicalize to the same string."""
    return canonical_url(left) == canonical_url(right)


def url_fingerprint(url):
    """Return a compact fingerprint of scheme and host used in dedup keys."""
    parts = urlsplit(canonical_url(url))
    return "{scheme}://{host}".format(scheme=parts.scheme, host=parts.hostname or "")


__all__ = ["canonical_url", "urls_equal", "url_fingerprint"]
