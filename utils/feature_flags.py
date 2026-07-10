#!/usr/bin/env python3
"""Feature flag system with rules and targeting."""
from typing import Dict, Any, Optional, List, Callable
from enum import Enum
import time
import hashlib

class Strategy(Enum):
    ON = "on"
    OFF = "off"
    PERCENTAGE = "percentage"
    TARGETED = "targeted"

class FeatureFlag:
    def __init__(self, key: str, strategy: Strategy = Strategy.OFF,
                 percentage: int = 0, targets: Optional[List[str]] = None,
                 description: str = ""):
        self._key = key
        self._strategy = strategy
        self._percentage = percentage
        self._targets = set(targets or [])
        self._desc = description
        self._enabled = True
        self._created = time.time()
        self._updated = time.time()
        self._rules: List[Callable] = []

    @property
    def key(self) -> str:
        return self._key

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @property
    def enabled(self) -> bool:
        return self._enabled

    def enable(self) -> None:
        self._enabled = True
        self._updated = time.time()

    def disable(self) -> None:
        self._enabled = False
        self._updated = time.time()

    def set_strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy
        self._updated = time.time()

    def set_percentage(self, pct: int) -> None:
        self._percentage = max(0, min(100, pct))
        self._updated = time.time()

    def add_target(self, target: str) -> None:
        self._targets.add(target)
        self._updated = time.time()

    def remove_target(self, target: str) -> None:
        self._targets.discard(target)
        self._updated = time.time()

    def add_rule(self, rule: Callable) -> None:
        self._rules.append(rule)

    def evaluate(self, context: Optional[Dict] = None) -> bool:
        if not self._enabled:
            return False
        ctx = context or {}
        user_id = ctx.get("user_id", "")
        for rule in self._rules:
            try:
                if rule(ctx):
                    return True
            except Exception:
                continue
        if self._strategy == Strategy.ON:
            return True
        elif self._strategy == Strategy.OFF:
            return False
        elif self._strategy == Strategy.PERCENTAGE:
            if not user_id:
                return False
            hash_val = int(hashlib.md5(f"{self._key}:{user_id}".encode()).hexdigest(), 16)
            return (hash_val % 100) < self._percentage
        elif self._strategy == Strategy.TARGETED:
            return user_id in self._targets
        return False

    def to_dict(self) -> dict:
        return {
            "key": self._key,
            "strategy": self._strategy.value,
            "percentage": self._percentage,
            "targets": list(self._targets),
            "enabled": self._enabled,
            "description": self._desc,
        }

class FeatureFlagManager:
    def __init__(self):
        self._flags: Dict[str, FeatureFlag] = {}

    def create(self, key: str, strategy: Strategy = Strategy.OFF, **kwargs) -> FeatureFlag:
        flag = FeatureFlag(key, strategy, **kwargs)
        self._flags[key] = flag
        return flag

    def get(self, key: str) -> Optional[FeatureFlag]:
        return self._flags.get(key)

    def is_enabled(self, key: str, context: Optional[Dict] = None) -> bool:
        flag = self._flags.get(key)
        if flag is None:
            return False
        return flag.evaluate(context)

    def enable(self, key: str) -> bool:
        flag = self._flags.get(key)
        if flag:
            flag.enable()
            return True
        return False

    def disable(self, key: str) -> bool:
        flag = self._flags.get(key)
        if flag:
            flag.disable()
            return True
        return False

    def delete(self, key: str) -> bool:
        if key in self._flags:
            del self._flags[key]
            return True
        return False

    def list_flags(self) -> List[str]:
        return list(self._flags.keys())

    def export(self) -> List[dict]:
        return [f.to_dict() for f in self._flags.values()]

    def import_flags(self, flags: List[dict]) -> int:
        count = 0
        for f in flags:
            strategy = Strategy(f.get("strategy", "off"))
            flag = self.create(f["key"], strategy,
                              percentage=f.get("percentage", 0),
                              targets=f.get("targets", []),
                              description=f.get("description", ""))
            if f.get("enabled", True):
                flag.enable()
            else:
                flag.disable()
            count += 1
        return count

    def count(self) -> int:
        return len(self._flags)
