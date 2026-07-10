#!/usr/bin/env python3
"""AVL tree with self-balancing rotations."""
from typing import Any, Optional, List

class AVLNode:
    def __init__(self, val: Any):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self._root = None

    def _height(self, node): return node.height if node else 0
    def _balance(self, node): return self._height(node.left) - self._height(node.right) if node else 0

    def _rotate_right(self, z):
        y = z.left; T = y.right
        y.right = z; z.left = T
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def _rotate_left(self, z):
        y = z.right; T = y.left
        y.left = z; z.right = T
        z.height = 1 + max(self._height(z.left), self._height(z.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def insert(self, val): self._root = self._insert(self._root, val)

    def _insert(self, node, val):
        if not node: return AVLNode(val)
        if val < node.val: node.left = self._insert(node.left, val)
        else: node.right = self._insert(node.right, val)
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        bal = self._balance(node)
        if bal > 1 and val < node.left.val: return self._rotate_right(node)
        if bal < -1 and val > node.right.val: return self._rotate_left(node)
        if bal > 1 and val > node.left.val:
            node.left = self._rotate_left(node.left); return self._rotate_right(node)
        if bal < -1 and val < node.right.val:
            node.right = self._rotate_right(node.right); return self._rotate_left(node)
        return node

    def inorder(self):
        result = []; self._inorder(self._root, result); return result

    def _inorder(self, node, result):
        if node: self._inorder(node.left, result); result.append(node.val); self._inorder(node.right, result)
