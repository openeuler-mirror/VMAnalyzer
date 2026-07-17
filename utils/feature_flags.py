#!/usr/bin/env python3
"""Feature flag toggle management for gradual rollout."""
import json
from typing import Dict, Optional

class FeatureFlags:
    """Manages feature flags with optional persistence."""

    def __init__(self, persist_path: Optional[str] = None):
        self._flags: Dict[str, bool] = {}
        self._persist_path = persist_path
        if persist_path:
            self._load()

    def enable(self, name: str) -> None:
        """Enable a feature flag."""
        self._flags[name] = True
        self._save()

    def disable(self, name: str) -> None:
        """Disable a feature flag."""
        self._flags[name] = False
        self._save()

    def is_enabled(self, name: str, default: bool = False) -> bool:
        """Check if a flag is enabled."""
        return self._flags.get(name, default)

    def toggle(self, name: str) -> bool:
        """Toggle a flag and return new state."""
        self._flags[name] = not self._flags.get(name, False)
        self._save()
        return self._flags[name]

    def list_flags(self) -> Dict[str, bool]:
        """Return all flags and their states."""
        return dict(self._flags)

    def _save(self) -> None:
        if self._persist_path:
            with open(self._persist_path, "w") as f:
                json.dump(self._flags, f)

    def _load(self) -> None:
        try:
            with open(self._persist_path, "r") as f:
                self._flags = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._flags = {}
