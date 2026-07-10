#!/usr/bin/env python3
"""Mediator pattern for decoupled component communication."""
from typing import Dict, List, Any, Callable, Optional, Set
from collections import defaultdict
import threading

class Colleague:
    def __init__(self, name: str, mediator: Optional["Mediator"] = None):
        self._name = name
        self._mediator = mediator
        self._handlers: Dict[str, Callable] = {}

    @property
    def name(self) -> str:
        return self._name

    def set_mediator(self, mediator: "Mediator") -> None:
        self._mediator = mediator

    def register_handler(self, message_type: str, handler: Callable) -> None:
        self._handlers[message_type] = handler

    def send(self, message_type: str, data: Any = None, target: Optional[str] = None) -> Any:
        if self._mediator:
            return self._mediator.dispatch(self, message_type, data, target)
        return None

    def broadcast(self, message_type: str, data: Any = None) -> List[Any]:
        if self._mediator:
            return self._mediator.broadcast(self, message_type, data)
        return []

    def receive(self, message_type: str, data: Any, sender: "Colleague") -> Any:
        handler = self._handlers.get(message_type)
        if handler:
            return handler(data, sender)
        return None

class Mediator:
    def __init__(self):
        self._colleagues: Dict[str, Colleague] = {}
        self._lock = threading.Lock()
        self._message_log: List[dict] = []
        self._interceptors: List[Callable] = []
        self._routing: Dict[str, Set[str]] = defaultdict(set)

    def register(self, colleague: Colleague) -> None:
        with self._lock:
            colleague.set_mediator(self)
            self._colleagues[colleague.name] = colleague

    def unregister(self, name: str) -> bool:
        with self._lock:
            if name in self._colleagues:
                self._colleagues[name].set_mediator(None)
                del self._colleagues[name]
                return True
            return False

    def dispatch(self, sender: Colleague, message_type: str,
                 data: Any = None, target: Optional[str] = None) -> Any:
        for interceptor in self._interceptors:
            if not interceptor(sender, message_type, data, target):
                return None
        with self._lock:
            self._message_log.append({
                "sender": sender.name, "type": message_type,
                "target": target, "timestamp": threading.get_ident()
            })
            if target:
                colleague = self._colleagues.get(target)
                if colleague and target in self._routing.get(message_type, {target}):
                    return colleague.receive(message_type, data, sender)
                return None
            else:
                for name, colleague in self._colleagues.items():
                    if name != sender.name:
                        if not self._routing or name in self._routing.get(message_type, set()):
                            result = colleague.receive(message_type, data, sender)
                            if result is not None:
                                return result
        return None

    def broadcast(self, sender: Colleague, message_type: str, data: Any = None) -> List[Any]:
        results = []
        with self._lock:
            colleagues = [(n, c) for n, c in self._colleagues.items() if n != sender.name]
        for name, colleague in colleagues:
            result = colleague.receive(message_type, data, sender)
            if result is not None:
                results.append(result)
        return results

    def add_route(self, message_type: str, target: str) -> None:
        self._routing[message_type].add(target)

    def add_interceptor(self, interceptor: Callable) -> None:
        self._interceptors.append(interceptor)

    def get_colleague(self, name: str) -> Optional[Colleague]:
        return self._colleagues.get(name)

    def list_colleagues(self) -> List[str]:
        return list(self._colleagues.keys())

    @property
    def colleague_count(self) -> int:
        return len(self._colleagues)

    @property
    def message_log(self) -> List[dict]:
        return list(self._message_log)

    def clear_log(self) -> None:
        with self._lock:
            self._message_log.clear()
