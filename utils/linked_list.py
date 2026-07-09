#!/usr/bin/env python3
"""Doubly linked list with traversal and manipulation."""
from typing import Any, Optional, List

class Node:
    def __init__(self, data: Any):
        self.data = data
        self.prev = None
        self.next = None

class LinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def append(self, data: Any) -> None:
        node = Node(data)
        if self._tail is None:
            self._head = self._tail = node
        else:
            node.prev = self._tail
            self._tail.next = node
            self._tail = node
        self._size += 1

    def prepend(self, data: Any) -> None:
        node = Node(data)
        if self._head is None:
            self._head = self._tail = node
        else:
            node.next = self._head
            self._head.prev = node
            self._head = node
        self._size += 1

    def remove(self, data: Any) -> bool:
        curr = self._head
        while curr:
            if curr.data == data:
                if curr.prev: curr.prev.next = curr.next
                else: self._head = curr.next
                if curr.next: curr.next.prev = curr.prev
                else: self._tail = curr.prev
                self._size -= 1
                return True
            curr = curr.next
        return False

    def to_list(self) -> List[Any]:
        result, curr = [], self._head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def size(self) -> int:
        return self._size
