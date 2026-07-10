#!/usr/bin/env python3
"""Binary search tree with insert, search, and traversal."""
from typing import Any, Optional, List

class TreeNode:
    def __init__(self, val: Any):
        self.val = val
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self._root = None

    def insert(self, val: Any) -> None:
        self._root = self._insert(self._root, val)

    def _insert(self, node: Optional[TreeNode], val: Any) -> TreeNode:
        if node is None:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        else:
            node.right = self._insert(node.right, val)
        return node

    def search(self, val: Any) -> bool:
        return self._search(self._root, val)

    def _search(self, node: Optional[TreeNode], val: Any) -> bool:
        if node is None:
            return False
        if val == node.val:
            return True
        return self._search(node.left if val < node.val else node.right, val)

    def inorder(self) -> List[Any]:
        result = []
        self._inorder(self._root, result)
        return result

    def _inorder(self, node: Optional[TreeNode], result: List) -> None:
        if node:
            self._inorder(node.left, result)
            result.append(node.val)
            self._inorder(node.right, result)
