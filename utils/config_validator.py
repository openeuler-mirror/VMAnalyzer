#!/usr/bin/env python3
"""Validate configuration schemas for required fields and types."""
from typing import Any, Dict, List

class ConfigValidator:
    """Validates configuration against a schema."""

    def __init__(self):
        self._schema: Dict[str, dict] = {}

    def add_field(self, name: str, field_type: type,
                  required: bool = True, default: Any = None) -> None:
        """Define a field in the schema."""
        self._schema[name] = {
            "type": field_type, "required": required, "default": default,
        }

    def validate(self, config: Dict[str, Any]) -> List[str]:
        """Validate config and return list of errors."""
        errors = []
        for name, spec in self._schema.items():
            if name not in config:
                if spec["required"]:
                    errors.append(f"Missing required field: {name}")
                continue
            val = config[name]
            if not isinstance(val, spec["type"]):
                errors.append(f"Field '{name}' must be {spec['type'].__name__}")
        for name in config:
            if name not in self._schema:
                errors.append(f"Unknown field: {name}")
        return errors

    def apply_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply default values for missing optional fields."""
        result = dict(config)
        for name, spec in self._schema.items():
            if name not in result and spec["default"] is not None:
                result[name] = spec["default"]
        return result
