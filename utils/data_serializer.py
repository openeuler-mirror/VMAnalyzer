#!/usr/bin/env python3
"""Data serialization utilities for multiple formats."""
import json
import pickle
from typing import Any

class DataSerializer:
    """Serializes and deserializes data in multiple formats."""

    @staticmethod
    def to_json(obj: Any) -> str:
        """Serialize to JSON string."""
        return json.dumps(obj, default=str, ensure_ascii=False)

    @staticmethod
    def from_json(data: str) -> Any:
        """Deserialize from JSON string."""
        return json.loads(data)

    @staticmethod
    def to_bytes(obj: Any) -> bytes:
        """Serialize to bytes using pickle."""
        return pickle.dumps(obj)

    @staticmethod
    def from_bytes(data: bytes) -> Any:
        """Deserialize from bytes."""
        return pickle.loads(data)

    @staticmethod
    def to_dict(obj: Any) -> dict:
        """Convert object to dictionary."""
        if isinstance(obj, dict):
            return obj
        if hasattr(obj, "__dict__"):
            return {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
        return {"value": str(obj)}

    @staticmethod
    def merge_dicts(*dicts: dict) -> dict:
        """Merge multiple dictionaries."""
        result = {}
        for d in dicts:
            result.update(d)
        return result
