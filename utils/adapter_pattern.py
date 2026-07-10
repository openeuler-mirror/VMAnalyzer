#!/usr/bin/env python3
"""Adapter pattern for interface compatibility."""
from typing import Any, Dict, List

class LegacyLogger:
    def write_message(self, msg: str) -> None:
        print(f"[LEGACY] {msg}")

    def write_error(self, err: str) -> None:
        print(f"[LEGACY ERROR] {err}")

class ModernLogInterface:
    def log(self, level: str, message: str, context: Dict = None) -> None:
        raise NotImplementedError

class JSONLogger(ModernLogInterface):
    def log(self, level: str, message: str, context: Dict = None) -> None:
        import json
        entry = {"level": level, "message": message, "context": context or {}}
        print(json.dumps(entry))

class LoggerAdapter(ModernLogInterface):
    def __init__(self, legacy: LegacyLogger):
        self._legacy = legacy

    def log(self, level: str, message: str, context: Dict = None) -> None:
        if level.upper() == "ERROR":
            self._legacy.write_error(message)
        else:
            self._legacy.write_message(f"[{level}] {message}")

class LogManager:
    def __init__(self):
        self._loggers: List[ModernLogInterface] = []

    def add_logger(self, logger: ModernLogInterface) -> None:
        self._loggers.append(logger)

    def log(self, level: str, message: str, context: Dict = None) -> None:
        for logger in self._loggers:
            logger.log(level, message, context)

    def info(self, message: str) -> None:
        self.log("INFO", message)

    def error(self, message: str) -> None:
        self.log("ERROR", message)
