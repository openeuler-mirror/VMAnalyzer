#!/usr/bin/env python3
"""Merge sort implementation with custom comparator."""
from typing import List, Callable, Any

def merge_sort(arr: List[Any], comparator: Callable = None) -> List[Any]:
    cmp = comparator or (lambda a, b: a < b)
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], cmp)
    right = merge_sort(arr[mid:], cmp)
    return _merge(left, right, cmp)

def _merge(left: List, right: List, cmp: Callable) -> List:
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if cmp(left[i], right[j]):
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def is_sorted(arr: List[Any], comparator: Callable = None) -> bool:
    cmp = comparator or (lambda a, b: a <= b)
    return all(cmp(arr[i], arr[i+1]) for i in range(len(arr)-1))

def binary_search(arr: List[Any], target: Any) -> int:
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
