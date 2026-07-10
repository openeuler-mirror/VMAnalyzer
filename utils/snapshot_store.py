#!/usr/bin/env python3
"""Snapshot store for periodic state persistence."""
from typing import Any, Dict, List, Optional, Callable
import time
import threading
import json
import os
from collections import OrderedDict

class Snapshot:
    def __init__(self, id: str, state: Any, version: int = 0,
                 metadata: Optional[Dict] = None):
        self._id = id
        self._state = state
        self._version = version
        self._metadata = metadata or {}
        self._timestamp = time.time()
        self._size = len(json.dumps(state, default=str)) if state else 0

    @property
    def id(self) -> str:
        return self._id

    @property
    def state(self) -> Any:
        return self._state

    @property
    def version(self) -> int:
        return self._version

    @property
    def metadata(self) -> Dict:
        return dict(self._metadata)

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def size(self) -> int:
        return self._size

    def to_dict(self) -> Dict:
        return {
            "id": self._id,
            "state": self._state,
            "version": self._version,
            "metadata": self._metadata,
            "timestamp": self._timestamp,
            "size": self._size,
        }

class SnapshotStore:
    def __init__(self, max_snapshots_per_stream: int = 10,
                 storage_dir: Optional[str] = None):
        self._snapshots: Dict[str, OrderedDict] = {}
        self._max_per_stream = max_snapshots_per_stream
        self._storage_dir = storage_dir
        self._lock = threading.Lock()
        self._stats = {"created": 0, "loaded": 0, "deleted": 0}
        if storage_dir:
            os.makedirs(storage_dir, exist_ok=True)

    def save_snapshot(self, stream_id: str, state: Any,
                      version: int = 0, metadata: Optional[Dict] = None) -> Snapshot:
        snapshot = Snapshot(f"{stream_id}_{int(time.time()*1000)}", state, version, metadata)
        with self._lock:
            if stream_id not in self._snapshots:
                self._snapshots[stream_id] = OrderedDict()
            self._snapshots[stream_id][snapshot.id] = snapshot
            while len(self._snapshots[stream_id]) > self._max_per_stream:
                _, evicted = self._snapshots[stream_id].popitem(last=False)
                self._stats["deleted"] += 1
                if self._storage_dir:
                    self._delete_from_disk(evicted)
            self._stats["created"] += 1
        if self._storage_dir:
            self._save_to_disk(snapshot)
        return snapshot

    def get_latest(self, stream_id: str) -> Optional[Snapshot]:
        with self._lock:
            snapshots = self._snapshots.get(stream_id)
            if not snapshots:
                return None
            return next(reversed(snapshots.values()))

    def get_snapshot(self, stream_id: str, snapshot_id: str) -> Optional[Snapshot]:
        with self._lock:
            snapshots = self._snapshots.get(stream_id)
            if snapshots:
                return snapshots.get(snapshot_id)
        return None

    def get_all(self, stream_id: str) -> List[Snapshot]:
        with self._lock:
            snapshots = self._snapshots.get(stream_id, {})
            return list(snapshots.values())

    def delete_snapshot(self, stream_id: str, snapshot_id: str) -> bool:
        with self._lock:
            snapshots = self._snapshots.get(stream_id)
            if snapshots and snapshot_id in snapshots:
                snapshot = snapshots.pop(snapshot_id)
                self._stats["deleted"] += 1
                if self._storage_dir:
                    self._delete_from_disk(snapshot)
                return True
            return False

    def delete_stream(self, stream_id: str) -> int:
        with self._lock:
            snapshots = self._snapshots.pop(stream_id, {})
            count = len(snapshots)
            self._stats["deleted"] += count
        if self._storage_dir:
            for snapshot in snapshots.values():
                self._delete_from_disk(snapshot)
        return count

    def stream_ids(self) -> List[str]:
        with self._lock:
            return list(self._snapshots.keys())

    def snapshot_count(self, stream_id: Optional[str] = None) -> int:
        with self._lock:
            if stream_id:
                return len(self._snapshots.get(stream_id, {}))
            return sum(len(s) for s in self._snapshots.values())

    @property
    def stats(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._stats)

    def _save_to_disk(self, snapshot: Snapshot) -> None:
        if not self._storage_dir:
            return
        filepath = os.path.join(self._storage_dir, f"{snapshot.id}.json")
        with open(filepath, "w") as f:
            json.dump(snapshot.to_dict(), f, indent=2)

    def _delete_from_disk(self, snapshot: Snapshot) -> None:
        if not self._storage_dir:
            return
        filepath = os.path.join(self._storage_dir, f"{snapshot.id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)

    def load_from_disk(self) -> int:
        if not self._storage_dir:
            return 0
        count = 0
        for filename in os.listdir(self._storage_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(self._storage_dir, filename)
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                    snapshot = Snapshot(
                        data["id"], data["state"],
                        data.get("version", 0), data.get("metadata")
                    )
                    snapshot._timestamp = data.get("timestamp", time.time())
                    stream_id = data["id"].rsplit("_", 1)[0]
                    with self._lock:
                        if stream_id not in self._snapshots:
                            self._snapshots[stream_id] = OrderedDict()
                        self._snapshots[stream_id][snapshot.id] = snapshot
                    count += 1
                except Exception:
                    pass
        self._stats["loaded"] += count
        return count

    def clear(self) -> None:
        with self._lock:
            self._snapshots.clear()
