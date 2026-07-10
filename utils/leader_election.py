#!/usr/bin/env python3
"""Leader election using Bully algorithm variant."""
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
import threading
import random

class NodeState(Enum):
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"

@dataclass
class ElectionNode:
    node_id: str
    priority: int
    state: NodeState = NodeState.FOLLOWER
    current_leader: Optional[str] = None
    term: int = 0
    last_seen: float = field(default_factory=time.time)
    voted_for: Optional[str] = None

class LeaderElection:
    def __init__(self, node_id: str, priority: int,
                 election_timeout: float = 5.0,
                 heartbeat_interval: float = 1.5):
        self._node = ElectionNode(node_id=node_id, priority=priority)
        self._peers: Dict[str, ElectionNode] = {}
        self._election_timeout = election_timeout
        self._heartbeat_interval = heartbeat_interval
        self._lock = threading.Lock()
        self._running = False
        self._callbacks: Dict[str, List[Callable]] = {
            "elected": [], "deposed": [], "timeout": []
        }
        self._last_heartbeat = time.time()
        self._thread: Optional[threading.Thread] = None

    def add_peer(self, node_id: str, priority: int) -> None:
        with self._lock:
            self._peers[node_id] = ElectionNode(node_id=node_id, priority=priority)

    def remove_peer(self, node_id: str) -> None:
        with self._lock:
            self._peers.pop(node_id, None)

    def receive_heartbeat(self, leader_id: str, term: int) -> None:
        with self._lock:
            if term >= self._node.term:
                self._node.term = term
                self._node.state = NodeState.FOLLOWER
                self._node.current_leader = leader_id
                self._node.voted_for = None
                self._last_heartbeat = time.time()

    def receive_vote_request(self, candidate_id: str, term: int) -> bool:
        with self._lock:
            if term > self._node.term:
                self._node.term = term
                self._node.state = NodeState.FOLLOWER
                self._node.voted_for = None
            if (term == self._node.term and
                (self._node.voted_for is None or
                 self._node.voted_for == candidate_id)):
                self._node.voted_for = candidate_id
                self._last_heartbeat = time.time()
                return True
            return False

    def receive_vote(self, voter_id: str, term: int) -> None:
        with self._lock:
            if (self._node.state == NodeState.CANDIDATE and
                term == self._node.term):
                self._peers.get(voter_id, ElectionNode("", 0)).voted_for = self._node.node_id
                votes = sum(1 for p in self._peers.values()
                           if p.voted_for == self._node.node_id) + 1
                total = len(self._peers) + 1
                if votes > total // 2:
                    self._node.state = NodeState.LEADER
                    self._node.current_leader = self._node.node_id
                    self._fire("elected", self._node)

    def _start_election(self) -> None:
        with self._lock:
            self._node.state = NodeState.CANDIDATE
            self._node.term += 1
            self._node.voted_for = self._node.node_id
            for peer in self._peers.values():
                peer.voted_for = None
        votes = 1
        for peer_id in list(self._peers.keys()):
            if self.receive_vote_request(peer_id, self._node.term):
                pass

    def _run(self) -> None:
        while self._running:
            time.sleep(0.5)
            with self._lock:
                state = self._node.state
            if state == NodeState.LEADER:
                time.sleep(self._heartbeat_interval)
            else:
                if time.time() - self._last_heartbeat > self._election_timeout:
                    self._start_election()

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)

    def on_event(self, event: str, callback: Callable) -> None:
        if event in self._callbacks:
            self._callbacks[event].append(callback)

    def _fire(self, event: str, node: ElectionNode) -> None:
        for cb in self._callbacks.get(event, []):
            try:
                cb(node)
            except Exception:
                pass

    @property
    def is_leader(self) -> bool:
        return self._node.state == NodeState.LEADER

    @property
    def leader_id(self) -> Optional[str]:
        return self._node.current_leader
