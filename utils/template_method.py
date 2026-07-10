#!/usr/bin/env python3
"""Template method pattern for algorithm skeletons."""
from abc import ABC, abstractmethod
from typing import List, Any

class DataProcessor(ABC):
    def process(self, data: List[Any]) -> List[Any]:
        data = self.load(data)
        data = self.validate(data)
        data = self.transform(data)
        data = self.filter(data)
        result = self.output(data)
        self.cleanup()
        return result

    @abstractmethod
    def load(self, data: List[Any]) -> List[Any]:
        pass

    def validate(self, data: List[Any]) -> List[Any]:
        return [d for d in data if d is not None]

    @abstractmethod
    def transform(self, data: List[Any]) -> List[Any]:
        pass

    def filter(self, data: List[Any]) -> List[Any]:
        return data

    def output(self, data: List[Any]) -> List[Any]:
        return list(data)

    def cleanup(self) -> None:
        pass

class NumericProcessor(DataProcessor):
    def load(self, data: List[Any]) -> List[Any]:
        return [float(d) if isinstance(d, (int, float, str)) else d for d in data]

    def validate(self, data: List[Any]) -> List[Any]:
        return [d for d in data if isinstance(d, (int, float)) and d == d]

    def transform(self, data: List[Any]) -> List[Any]:
        return [d * 2 for d in data]

    def filter(self, data: List[Any]) -> List[Any]:
        avg = sum(data) / len(data) if data else 0
        return [d for d in data if d > avg]

class StringProcessor(DataProcessor):
    def load(self, data: List[Any]) -> List[Any]:
        return [str(d) for d in data]

    def validate(self, data: List[Any]) -> List[Any]:
        return [d for d in data if d.strip()]

    def transform(self, data: List[Any]) -> List[Any]:
        return [d.strip().upper() for d in data]

    def filter(self, data: List[Any]) -> List[Any]:
        seen = set()
        result = []
        for d in data:
            if d not in seen:
                seen.add(d)
                result.append(d)
        return result

    def cleanup(self) -> None:
        pass
