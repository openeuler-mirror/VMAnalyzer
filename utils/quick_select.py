#!/usr/bin/env python3
"""Quickselect algorithm for finding kth smallest element."""
import random
from typing import List, Any

def quickselect(arr: List[Any], k: int) -> Any:
    if not arr or k < 0 or k >= len(arr):
        raise ValueError("Invalid k")
    return _select(arr[:], 0, len(arr) - 1, k)

def _select(arr: List, lo: int, hi: int, k: int) -> Any:
    if lo == hi:
        return arr[lo]
    pivot_idx = random.randint(lo, hi)
    pivot_idx = _partition(arr, lo, hi, pivot_idx)
    if k == pivot_idx:
        return arr[k]
    elif k < pivot_idx:
        return _select(arr, lo, pivot_idx - 1, k)
    else:
        return _select(arr, pivot_idx + 1, hi, k)

def _partition(arr: List, lo: int, hi: int, pivot_idx: int) -> int:
    pivot_val = arr[pivot_idx]
    arr[pivot_idx], arr[hi] = arr[hi], arr[pivot_idx]
    store_idx = lo
    for i in range(lo, hi):
        if arr[i] < pivot_val:
            arr[i], arr[store_idx] = arr[store_idx], arr[i]
            store_idx += 1
    arr[store_idx], arr[hi] = arr[hi], arr[store_idx]
    return store_idx

def median(arr: List[Any]) -> Any:
    n = len(arr)
    if n % 2 == 1:
        return quickselect(arr, n // 2)
    a = quickselect(arr, n // 2 - 1)
    b = quickselect(arr, n // 2)
    return (a + b) / 2
