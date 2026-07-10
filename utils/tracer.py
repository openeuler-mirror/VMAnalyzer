#!/usr/bin/env python3
"""Distributed tracer for request flow tracing."""
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import threading
import uuid
from collections import defaultdict

class SpanStatus(Enum):
    STARTED = "started"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class Span:
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    operation_name: str
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    status: SpanStatus = SpanStatus.STARTED
    tags: Dict[str, Any] = field(default_factory=dict)
    logs: List[Dict[str, Any]] = field(default_factory=list)
    baggage: Dict[str, str] = field(default_factory=dict)

    def set_tag(self, key: str, value: Any) -> None:
        self.tags[key] = value

    def log(self, message: str, level: str = "INFO", **kwargs) -> None:
        self.logs.append({
            "timestamp": time.time(),
            "level": level,
            "message": message,
            **kwargs
        })

    def finish(self, status: SpanStatus = SpanStatus.COMPLETED) -> None:
        self.end_time = time.time()
        self.status = status

    @property
    def duration(self) -> Optional[float]:
        if self.end_time:
            return self.end_time - self.start_time
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent_span_id": self.parent_span_id,
            "operation_name": self.operation_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "status": self.status.value,
            "tags": dict(self.tags),
            "logs": list(self.logs),
        }

class TraceContext:
    def __init__(self, trace_id: str, span_id: str,
                 parent_span_id: Optional[str] = None,
                 baggage: Optional[Dict[str, str]] = None):
        self._trace_id = trace_id
        self._span_id = span_id
        self._parent_span_id = parent_span_id
        self._baggage = baggage or {}

    @property
    def trace_id(self) -> str:
        return self._trace_id

    @property
    def span_id(self) -> str:
        return self._span_id

    @property
    def parent_span_id(self) -> Optional[str]:
        return self._parent_span_id

    def get_baggage(self, key: str) -> Optional[str]:
        return self._baggage.get(key)

    def set_baggage(self, key: str, value: str) -> None:
        self._baggage[key] = value

    def to_headers(self) -> Dict[str, str]:
        headers = {
            "x-trace-id": self._trace_id,
            "x-span-id": self._span_id,
        }
        if self._parent_span_id:
            headers["x-parent-span-id"] = self._parent_span_id
        for k, v in self._baggage.items():
            headers[f"x-baggage-{k}"] = v
        return headers

    @classmethod
    def from_headers(cls, headers: Dict[str, str]) -> "TraceContext":
        trace_id = headers.get("x-trace-id", str(uuid.uuid4()))
        span_id = headers.get("x-span-id", str(uuid.uuid4()))
        parent = headers.get("x-parent-span-id")
        baggage = {}
        for k, v in headers.items():
            if k.startswith("x-baggage-"):
                baggage[k[10:]] = v
        return cls(trace_id, span_id, parent, baggage)

class Tracer:
    _local = threading.local()

    def __init__(self, service_name: str = "default"):
        self._service_name = service_name
        self._spans: List[Span] = []
        self._lock = threading.Lock()
        self._span_reporters: List[Callable] = []
        self._stats = {"spans_created": 0, "spans_completed": 0, "errors": 0}

    def start_span(self, operation_name: str,
                   child_of: Optional[Span] = None) -> Span:
        if child_of:
            trace_id = child_of.trace_id
            parent_id = child_of.span_id
        else:
            trace_id = str(uuid.uuid4())
            parent_id = None
        span = Span(
            span_id=str(uuid.uuid4()),
            trace_id=trace_id,
            parent_span_id=parent_id,
            operation_name=operation_name,
        )
        span.set_tag("service", self._service_name)
        with self._lock:
            self._spans.append(span)
            self._stats["spans_created"] += 1
        self._push_span(span)
        return span

    def finish_span(self, span: Span, error: Optional[Exception] = None) -> None:
        if error:
            span.finish(SpanStatus.ERROR)
            span.set_tag("error", True)
            span.set_tag("error.message", str(error))
            with self._lock:
                self._stats["errors"] += 1
        else:
            span.finish(SpanStatus.COMPLETED)
        with self._lock:
            self._stats["spans_completed"] += 1
        for reporter in self._span_reporters:
            try:
                reporter(span)
            except Exception:
                pass
        self._pop_span()

    def current_span(self) -> Optional[Span]:
        return getattr(self._local, "span_stack", [None])[-1]

    def _push_span(self, span: Span) -> None:
        if not hasattr(self._local, "span_stack"):
            self._local.span_stack = []
        self._local.span_stack.append(span)

    def _pop_span(self) -> None:
        if hasattr(self._local, "span_stack") and self._local.span_stack:
            self._local.span_stack.pop()

    def add_reporter(self, reporter: Callable) -> None:
        self._span_reporters.append(reporter)

    def get_trace(self, trace_id: str) -> List[Span]:
        with self._lock:
            return [s for s in self._spans if s.trace_id == trace_id]

    def get_all_spans(self) -> List[Span]:
        with self._lock:
            return list(self._spans)

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    @property
    def span_count(self) -> int:
        with self._lock:
            return len(self._spans)

    def clear(self) -> None:
        with self._lock:
            self._spans.clear()

    def export(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [s.to_dict() for s in self._spans]

class TraceSpanContext:
    def __init__(self, tracer: Tracer, operation_name: str,
                 parent: Optional[Span] = None):
        self._tracer = tracer
        self._operation = operation_name
        self._parent = parent
        self._span: Optional[Span] = None

    def __enter__(self) -> Span:
        self._span = self._tracer.start_span(self._operation, self._parent)
        return self._span

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._span:
            self._tracer.finish_span(self._span, exc_val if exc_type else None)
        return False
