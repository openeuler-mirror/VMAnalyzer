"""Coarse User-Agent family detection based on substring signatures."""

_SIGNATURES = (
    ("curl", "curl"),
    ("wget", "wget"),
    ("python-requests", "requests"),
    ("go-http-client", "go"),
    ("postmanruntime", "postman"),
    ("okhttp", "okhttp"),
    ("mozilla", "browser"),
)


def detect_family(user_agent):
    """Return a short family label for a User-Agent string."""
    lowered = (user_agent or "").lower()
    for needle, family in _SIGNATURES:
        if needle in lowered:
            return family
    return "unknown"


def is_bot(user_agent):
    """Return True when the agent advertises an automated crawler."""
    lowered = (user_agent or "").lower()
    return any(word in lowered for word in ("bot", "spider", "crawler", "slurp"))


def platform_hint(user_agent):
    """Return a best-effort platform hint, or ``unknown``."""
    lowered = (user_agent or "").lower()
    for token, platform in (("windows", "windows"), ("iphone", "ios"), ("android", "android"),
                            ("linux", "linux"), ("mac os", "macos")):
        if token in lowered:
            return platform
    return "unknown"


__all__ = ["detect_family", "is_bot", "platform_hint"]
