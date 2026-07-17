#!/usr/bin/env python3
"""File path resolution utility for consistent path handling."""
import os
from typing import List, Optional

class PathResolver:
    """Resolves and normalizes file paths with base directory support."""

    def __init__(self, base_dir: str = "/"):
        self._base = os.path.abspath(base_dir)

    def resolve(self, path: str) -> str:
        """Resolve a path relative to base directory."""
        if os.path.isabs(path):
            return os.path.normpath(path)
        return os.path.normpath(os.path.join(self._base, path))

    def ensure_dir(self, path: str) -> str:
        """Ensure directory exists, creating if needed."""
        full = self.resolve(path)
        os.makedirs(full, exist_ok=True)
        return full

    def exists(self, path: str) -> bool:
        """Check if path exists."""
        return os.path.exists(self.resolve(path))

    def join(self, *paths: str) -> str:
        """Join path components."""
        return self.resolve(os.path.join(*paths))

    def relative(self, path: str) -> str:
        """Return path relative to base directory."""
        return os.path.relpath(self.resolve(path), self._base)

    def list_files(self, path: str, pattern: str = "*") -> List[str]:
        """List files matching pattern in directory."""
        import glob
        full = self.resolve(path)
        return sorted(glob.glob(os.path.join(full, pattern)))
