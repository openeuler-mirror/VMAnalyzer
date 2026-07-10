#!/usr/bin/env python3
"""Builder pattern for constructing complex configurations."""
from typing import Any, Dict, List, Optional

class ConfigBuilder:
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._sections: Dict[str, Dict] = {}
        self._validators: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> "ConfigBuilder":
        self._data[key] = value
        return self

    def add_section(self, name: str) -> "ConfigBuilder":
        self._sections[name] = {}
        return self

    def set_in_section(self, section: str, key: str, value: Any) -> "ConfigBuilder":
        if section not in self._sections:
            self._sections[section] = {}
        self._sections[section][key] = value
        return self

    def add_validator(self, key: str, validator: Any) -> "ConfigBuilder":
        self._validators[key] = validator
        return self

    def build(self) -> Dict[str, Any]:
        result = dict(self._data)
        result["sections"] = dict(self._sections)
        for key, validator in self._validators.items():
            if key in result and not validator(result[key]):
                raise ValueError(f"Validation failed for {key}")
        return result

    def reset(self) -> "ConfigBuilder":
        self._data.clear()
        self._sections.clear()
        self._validators.clear()
        return self

class ConfigDirector:
    def __init__(self, builder: ConfigBuilder):
        self._builder = builder

    def build_default(self) -> Dict[str, Any]:
        return (self._builder.reset()
                .set("version", "1.0")
                .set("debug", False)
                .add_section("database")
                .set_in_section("database", "host", "localhost")
                .set_in_section("database", "port", 5432)
                .build())
