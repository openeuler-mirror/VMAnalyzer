#!/usr/bin/env python3
"""Strategy pattern for interchangeable algorithms."""
from typing import List, Any, Protocol

class SortStrategy(Protocol):
    def sort(self, data: List[Any]) -> List[Any]: ...

class BubbleSort:
    def sort(self, data: List[Any]) -> List[Any]:
        arr = list(data)
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

class InsertionSort:
    def sort(self, data: List[Any]) -> List[Any]:
        arr = list(data)
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

class ShellSort:
    def sort(self, data: List[Any]) -> List[Any]:
        arr = list(data)
        n = len(arr)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2
        return arr

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def execute(self, data: List[Any]) -> List[Any]:
        return self._strategy.sort(data)
