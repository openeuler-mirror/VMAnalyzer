#!/usr/bin/env python3
"""Finite state machine with transition table."""
from typing import Any, Optional, Dict, Set, Callable

class StateMachine:
    def __init__(self, initial: str):
        self._current = initial
        self._transitions: Dict[str, Dict[str, str]] = {}
        self._handlers: Dict[str, Callable] = {}
        self._history: list = [initial]

    def add_transition(self, from_state: str, event: str, to_state: str) -> None:
        if from_state not in self._transitions:
            self._transitions[from_state] = {}
        self._transitions[from_state][event] = to_state

    def add_handler(self, state: str, handler: Callable) -> None:
        self._handlers[state] = handler

    def trigger(self, event: str) -> bool:
        trans = self._transitions.get(self._current, {})
        if event not in trans:
            return False
        old = self._current
        self._current = trans[event]
        self._history.append(self._current)
        handler = self._handlers.get(self._current)
        if handler:
            handler(old, event, self._current)
        return True

    @property
    def current(self) -> str:
        return self._current

    def can_trigger(self, event: str) -> bool:
        return event in self._transitions.get(self._current, {})

    def available_events(self) -> list:
        return list(self._transitions.get(self._current, {}).keys())

    def reset(self, state: str) -> None:
        self._current = state
        self._history = [state]

    def history(self) -> list:
        return list(self._history)
