#!/usr/bin/env python3
"""Resolve configuration values from environment variables."""
import os
from typing import Any, Dict, Optional

class EnvResolver:
    """Resolves configuration from environment with type casting."""

    def __init__(self, prefix: str = "VMANALYZER_"):
        self._prefix = prefix
        self._overrides: Dict[str, Any] = {}

    def get(self, key: str, default: Any = None,
            cast_type: type = str) -> Any:
        """Get a value from environment with type casting."""
        env_key = f"{self._prefix}{key.upper()}"
        if env_key in self._overrides:
            return self._overrides[env_key]
        val = os.environ.get(env_key)
        if val is None:
            return default
        try:
            if cast_type == bool:
                return val.lower() in ("true", "1", "yes")
            return cast_type(val)
        except (ValueError, TypeError):
            return default

    def set_override(self, key: str, value: Any) -> None:
        """Set a programmatic override."""
        env_key = f"{self._prefix}{key.upper()}"
        self._overrides[env_key] = value

    def resolve_all(self, config: dict) -> dict:
        """Override config dict values with environment variables."""
        result = dict(config)
        for key in list(result.keys()):
            env_val = self.get(key, cast_type=type(result[key]) if result[key] else str)
            if env_val is not None:
                result[key] = env_val
        return result
