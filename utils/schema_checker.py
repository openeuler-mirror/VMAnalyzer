#!/usr/bin/env python3
"""Schema validation for structured data."""
from typing import Any, Dict, List, Union

class SchemaChecker:
    """Validates data against a defined schema."""

    def __init__(self):
        self._schemas: Dict[str, Dict] = {}

    def define(self, name: str, fields: Dict[str, dict]) -> None:
        """Define a schema with field specifications."""
        self._schemas[name] = fields

    def validate(self, schema_name: str, data: dict) -> List[str]:
        """Validate data against schema, return errors."""
        errors = []
        schema = self._schemas.get(schema_name)
        if not schema:
            return [f"Unknown schema: {schema_name}"]
        for field, spec in schema.items():
            if field not in data:
                if spec.get("required", False):
                    errors.append(f"Missing required field: {field}")
                continue
            val = data[field]
            expected = spec.get("type")
            if expected and not isinstance(val, expected):
                errors.append(f"Field '{field}' must be {expected.__name__}")
            if "values" in spec and val not in spec["values"]:
                errors.append(f"Field '{field}' must be one of {spec['values']}")
        return errors

    def is_valid(self, schema_name: str, data: dict) -> bool:
        """Check if data is valid against schema."""
        return len(self.validate(schema_name, data)) == 0

    def list_schemas(self) -> List[str]:
        """Return all schema names."""
        return list(self._schemas.keys())
