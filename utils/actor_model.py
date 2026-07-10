#!/usr/bin/env python3
"""Actor model for concurrent message passing."""
from typing import Any, Callable, Dict, List, Optional
import threading
from queue import Queue
from enum import Enum

class ActorState(Enum):
    CREATED = "created"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"

class Message:
    def __init__(self, msg_type: str, payload: Any = None, sender: Optional["Actor"] = None):
        self._type = msg_type
        self._payload = payload
        self._sender = sender

    @property
    def type(self) -> str:
        return self._type

    @property
    def payload(self) -> Any:
        return self._payload

    @property
    def sender(self) -> Optional["Actor"]:
        return self._sender

class Actor:
    _id_counter = 0
    _id_lock = threading.Lock()

    def __init__(self, name: str = ""):
        with Actor._id_lock:
            Actor._id_counter += 1
            self._id = Actor._id_counter
        self._name = name or f"actor-{self._id}"
        self._mailbox: Queue = Queue()
        self._state = ActorState.CREATED
        self._handlers: Dict[str, Callable] = {}
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self._stats = {"received": 0, "processed": 0, "errors": 0}
        self._children: List[Actor] = []
        self._parent: Optional[Actor] = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> ActorState:
        return self._state

    def register_handler(self, msg_type: str, handler: Callable) -> None:
        self._handlers[msg_type] = handler

    def tell(self, msg_type: str, payload: Any = None,
             sender: Optional["Actor"] = None) -> bool:
        msg = Message(msg_type, payload, sender)
        try:
            self._mailbox.put_nowait(msg)
            return True
        except Exception:
            return False

    def ask(self, msg_type: str, payload: Any = None, timeout: float = 5.0) -> Any:
        response_queue: Queue = Queue()
        def handler_wrapper(msg: Message):
            handler = self._handlers.get(msg_type)
            if handler:
                try:
                    result = handler(msg.payload, msg.sender)
                    response_queue.put(result)
                except Exception as e:
                    response_queue.put(e)
        original = self._handlers.get(msg_type)
        self._handlers[msg_type] = lambda payload, sender: None
        self.tell(msg_type, payload)
        try:
            return response_queue.get(timeout=timeout)
        except Exception:
            return None
        finally:
            if original:
                self._handlers[msg_type] = original

    def start(self) -> None:
        if self._state == ActorState.RUNNING:
            return
        self._state = ActorState.RUNNING
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._state = ActorState.STOPPED
        self.tell("__stop__")
        if self._thread:
            self._thread.join(timeout=5)

    def _run(self) -> None:
        while self._state == ActorState.RUNNING:
            try:
                msg = self._mailbox.get(timeout=1)
                if msg.type == "__stop__":
                    break
                with self._lock:
                    self._stats["received"] += 1
                handler = self._handlers.get(msg.type)
                if handler:
                    try:
                        handler(msg.payload, msg.sender)
                        with self._lock:
                            self._stats["processed"] += 1
                    except Exception:
                        with self._lock:
                            self._stats["errors"] += 1
                            self._state = ActorState.ERROR
            except Exception:
                continue

    def create_child(self, name: str = "") -> "Actor":
        child = Actor(name)
        child._parent = self
        self._children.append(child)
        return child

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def mailbox_size(self) -> int:
        return self._mailbox.qsize()

    @property
    def children(self) -> List["Actor"]:
        return list(self._children)

class ActorSystem:
    def __init__(self):
        self._actors: Dict[int, Actor] = {}
        self._lock = threading.Lock()

    def create_actor(self, name: str = "") -> Actor:
        actor = Actor(name)
        with self._lock:
            self._actors[actor.id] = actor
        actor.start()
        return actor

    def get_actor(self, actor_id: int) -> Optional[Actor]:
        return self._actors.get(actor_id)

    def find_by_name(self, name: str) -> Optional[Actor]:
        for actor in self._actors.values():
            if actor.name == name:
                return actor
        return None

    def stop_all(self) -> None:
        with self._lock:
            actors = list(self._actors.values())
        for actor in actors:
            actor.stop()
        self._actors.clear()

    @property
    def actor_count(self) -> int:
        return len(self._actors)

    def list_actors(self) -> List[str]:
        return [a.name for a in self._actors.values()]
