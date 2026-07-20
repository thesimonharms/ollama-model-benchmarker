from abc import ABC, abstractmethod
from typing import Any

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self, response: str, expected: Any) -> bool:
        """Returns True if the response meets the criteria, False otherwise."""
        pass
