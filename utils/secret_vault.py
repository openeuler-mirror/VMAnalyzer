#!/usr/bin/env python3
"""Secret vault for secure credential management."""
from typing import Dict, Optional, Any
import hashlib
import os
import time
import json
from base64 import b64encode, b64decode

class Secret:
    def __init__(self, key: str, value: str, metadata: Optional[Dict] = None):
        self._key = key
        self._value = value
        self._metadata = metadata or {}
        self._created = time.time()
        self._updated = time.time()
        self._version = 1
        self._history: list = []

    @property
    def key(self) -> str:
        return self._key

    def get_value(self) -> str:
        return self._value

    def set_value(self, value: str) -> None:
        self._history.append({"value": self._value, "version": self._version, "time": self._updated})
        self._value = value
        self._version += 1
        self._updated = time.time()

    @property
    def version(self) -> int:
        return self._version

    @property
    def metadata(self) -> Dict:
        return dict(self._metadata)

    def add_metadata(self, key: str, value: Any) -> None:
        self._metadata[key] = value
        self._updated = time.time()

    @property
    def created_at(self) -> float:
        return self._created

    @property
    def updated_at(self) -> float:
        return self._updated

    def rollback(self, version: int) -> bool:
        for entry in self._history:
            if entry["version"] == version:
                self._history.append({"value": self._value, "version": self._version, "time": self._updated})
                self._value = entry["value"]
                self._version = entry["version"]
                self._updated = time.time()
                return True
        return False

    def history(self) -> list:
        return list(self._history)

class SecretVault:
    def __init__(self, master_key: Optional[str] = None):
        self._secrets: Dict[str, Secret] = {}
        self._master_key = master_key or os.urandom(32).hex()
        self._access_log: list = []
        self._encryption_enabled = bool(master_key)

    def _encrypt(self, value: str) -> str:
        if not self._encryption_enabled:
            return value
        key = hashlib.sha256(self._master_key.encode()).digest()
        result = bytearray()
        for i, byte in enumerate(value.encode()):
            result.append(byte ^ key[i % len(key)])
        return b64encode(bytes(result)).decode()

    def _decrypt(self, value: str) -> str:
        if not self._encryption_enabled:
            return value
        key = hashlib.sha256(self._master_key.encode()).digest()
        data = b64decode(value.encode())
        result = bytearray()
        for i, byte in enumerate(data):
            result.append(byte ^ key[i % len(key)])
        return result.decode()

    def put(self, key: str, value: str, metadata: Optional[Dict] = None) -> Secret:
        secret = Secret(key, value, metadata)
        self._secrets[key] = secret
        self._log_access("put", key)
        return secret

    def get(self, key: str) -> Optional[str]:
        secret = self._secrets.get(key)
        if secret is None:
            self._log_access("get_miss", key)
            return None
        self._log_access("get", key)
        return secret.get_value()

    def update(self, key: str, value: str) -> bool:
        secret = self._secrets.get(key)
        if secret is None:
            return False
        secret.set_value(value)
        self._log_access("update", key)
        return True

    def delete(self, key: str) -> bool:
        if key in self._secrets:
            del self._secrets[key]
            self._log_access("delete", key)
            return True
        return False

    def list_keys(self) -> list:
        return list(self._secrets.keys())

    def exists(self, key: str) -> bool:
        return key in self._secrets

    def get_secret(self, key: str) -> Optional[Secret]:
        return self._secrets.get(key)

    def export_encrypted(self) -> str:
        data = {k: {"value": self._encrypt(s.get_value()), "metadata": s.metadata,
                     "version": s.version} for k, s in self._secrets.items()}
        return json.dumps(data)

    def import_encrypted(self, data: str) -> int:
        decoded = json.loads(data)
        count = 0
        for key, info in decoded.items():
            value = self._decrypt(info["value"])
            secret = Secret(key, value, info.get("metadata"))
            secret._version = info.get("version", 1)
            self._secrets[key] = secret
            count += 1
        return count

    def _log_access(self, action: str, key: str) -> None:
        self._access_log.append({"action": action, "key": key, "time": time.time()})

    def access_log(self) -> list:
        return list(self._access_log)

    def count(self) -> int:
        return len(self._secrets)

    def clear(self) -> None:
        self._secrets.clear()
        self._access_log.clear()
