#!/usr/bin/env python3
"""Heartbeat monitor for detecting service liveness."""
from typing import Dict, Set, Callable, Optional, List
from dataclasses import dataclass, field
import time
import threading

@dataclass
class HeartbeatTarget:
    target_id: str
    interval: float
    timeout: float
    last_heartbeat: float = field(default_factory=time.time)
    consecutive_misses: int = 0
    alive: bool = True
    metadata: Dict[str, str] = field(default_factory=dict)

class HeartbeatMonitor:
    def __init__(self, max_misses: int = 3, check_interval: float = 5.0):
        self._targets: Dict[str, HeartbeatTarget] = {}
        self._max_misses = max_misses
        self._check_interval = check_interval
        self._lock = threading.Lock()
        self._callbacks: Dict[str, List[Callable]] = {
            "alive": [], "dead": [], "timeout": []
        }
        self._running = False
        self._monitor_thread: Optional[threading.Thread] = None

    def register(self, target_id: str, interval: float,
                 timeout: float, **metadata) -> HeartbeatTarget:
        target = HeartbeatTarget(
            target_id=target_id, interval=interval,
            timeout=timeout, metadata=dict(metadata)
        )
        with self._lock:
            self._targets[target_id] = target
        return target

    def unregister(self, target_id: str) -> bool:
        with self._lock:
            return self._targets.pop(target_id, None) is not None

    def ping(self, target_id: str) -> bool:
        with self._lock:
            target = self._targets.get(target_id)
            if target:
                target.last_heartbeat = time.time()
                target.consecutive_misses = 0
                if not target.alive:
                    target.alive = True
                    self._fire("alive", target)
                return True
            return False

    def _check_targets(self) -> None:
        now = time.time()
        with self._lock:
            for target in self._targets.values():
                elapsed = now - target.last_heartbeat
                if elapsed > target.timeout:
                    target.consecutive_misses += 1
                    if target.consecutive_misses >= self._max_misses:
                        if target.alive:
                            target.alive = False
                            self._fire("dead", target)
                    else:
                        self._fire("timeout", target)
                    target.last_heartbeat = now

    def start(self) -> None:
        self._running = True
        def _run():
            while self._running:
                time.sleep(self._check_interval)
                self._check_targets()
        self._monitor_thread = threading.Thread(target=_run, daemon=True)
        self._monitor_thread.start()

    def stop(self) -> None:
        self._running = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)

    def on_event(self, event_type: str, callback: Callable) -> None:
        if event_type in self._callbacks:
            self._callbacks[event_type].append(callback)

    def _fire(self, event_type: str, target: HeartbeatTarget) -> None:
        for cb in self._callbacks.get(event_type, []):
            try:
                cb(target)
            except Exception:
                pass

    def alive_targets(self) -> List[str]:
        with self._lock:
            return [t.target_id for t in self._targets.values() if t.alive]

    def dead_targets(self) -> List[str]:
        with self._lock:
            return [t.target_id for t in self._targets.values() if not t.alive]

    @property
    def target_count(self) -> int:
        with self._lock:
            return len(self._targets)
