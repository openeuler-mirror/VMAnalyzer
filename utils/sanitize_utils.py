#!/usr/bin/env python3
"""Data sanitization helpers for safe output and storage."""
import html
import re
from typing import Any, Dict

class SanitizeUtils:
    """Sanitizes data for safe handling and output."""

    @staticmethod
    def sanitize_html(text: str) -> str:
        return html.escape(text, quote=True)

    @staticmethod
    def sanitize_sql(text: str) -> str:
        return re.sub(r"[;'"\--]", "", text)

    @staticmethod
    def sanitize_filename(name: str) -> str:
        return re.sub(r"[^a-zA-Z0-9_\-.]", "_", name)

    @staticmethod
    def sanitize_dict(data: Dict[str, Any], max_depth: int = 10) -> Dict[str, Any]:
        if max_depth <= 0:
            return {"_truncated": True}
        result = {}
        for k, v in data.items():
            if isinstance(v, dict):
                result[k] = SanitizeUtils.sanitize_dict(v, max_depth - 1)
            elif isinstance(v, str):
                result[k] = SanitizeUtils.sanitize_html(v)
            else:
                result[k] = v
        return result

    @staticmethod
    def strip_ansi(text: str) -> str:
        return re.sub(r"\x1b\[[0-9;]*m", "", text)

    @staticmethod
    def truncate(text: str, max_len: int = 100) -> str:
        return text[:max_len] + "..." if len(text) > max_len else text
