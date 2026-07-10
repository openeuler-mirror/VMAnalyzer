#!/usr/bin/env python3
"""Configuration manager with layered overrides."""
from typing import Any, Dict, Optional, List, Callable
import json
import os
import copy

class ConfigLayer:
    def __init__(self, name: str, priority: int = 0):
        self._name = name
        self._priority = priority
        self._data: Dict[str, Any] = {}
        self._listeners: List[Callable] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def priority(self) -> int:
        return self._priority

    def set(self, key: str, value: Any) -> None:
        old = self._data.get(key)
        self._data[key] = value
        if old != value:
            self._notify(key, old, value)

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def has(self, key: str) -> bool:
        return key in self._data

    def remove(self, key: str) -> bool:
        if key in self._data:
            old = self._data.pop(key)
            self._notify(key, old, None)
            return True
        return False

    def keys(self) -> List[str]:
        return list(self._data.keys())

    def to_dict(self) -> Dict[str, Any]:
        return copy.deepcopy(self._data)

    def update(self, data: Dict[str, Any]) -> None:
        for k, v in data.items():
            self.set(k, v)

    def clear(self) -> None:
        self._data.clear()

    def add_listener(self, callback: Callable) -> None:
        self._listeners.append(callback)

    def _notify(self, key: str, old: Any, new: Any) -> None:
        for cb in self._listeners:
            cb(self._name, key, old, new)

class ConfigManager:
    def __init__(self):
        self._layers: Dict[str, ConfigLayer] = {}
        self._layers_list: List[ConfigLayer] = []

    def add_layer(self, name: str, priority: int = 0) -> ConfigLayer:
        layer = ConfigLayer(name, priority)
        self._layers[name] = layer
        self._layers_list.append(layer)
        self._layers_list.sort(key=lambda l: l.priority, reverse=True)
        return layer

    def get(self, key: str, default: Any = None) -> Any:
        for layer in self._layers_list:
            if layer.has(key):
                return layer.get(key)
        return default

    def set(self, key: str, value: Any, layer: str = "default") -> None:
        if layer not in self._layers:
            self.add_layer(layer)
        self._layers[layer].set(key, value)

    def has(self, key: str) -> bool:
        return any(layer.has(key) for layer in self._layers_list)

    def remove(self, key: str) -> bool:
        for layer in self._layers_list:
            if layer.remove(key):
                return True
        return False

    def all_keys(self) -> List[str]:
        keys = set()
        for layer in self._layers_list:
            keys.update(layer.keys())
        return sorted(keys)

    def to_dict(self) -> Dict[str, Any]:
        result = {}
        for layer in reversed(self._layers_list):
            result.update(layer.to_dict())
        return result

    def load_from_dict(self, data: Dict[str, Any], layer: str = "default") -> None:
        if layer not in self._layers:
            self.add_layer(layer)
        self._layers[layer].update(data)

    def load_from_json_file(self, filepath: str, layer: str = "file") -> None:
        if not os.path.isfile(filepath):
            return
        with open(filepath, "r") as f:
            data = json.load(f)
        self.load_from_dict(data, layer)

    def save_to_json(self, filepath: str) -> None:
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def layer_names(self) -> List[str]:
        return [l.name for l in self._layers_list]

    def get_layer(self, name: str) -> Optional[ConfigLayer]:
        return self._layers.get(name)

    def remove_layer(self, name: str) -> bool:
        if name not in self._layers:
            return False
        layer = self._layers.pop(name)
        self._layers_list.remove(layer)
        return True
