"""Strategy interface for output."""

from abc import ABC, abstractmethod


class IOutputStrategy(ABC):

    @abstractmethod
    def write(self, message: str) -> None:
        """Write a single message to the output destination."""

    @abstractmethod
    def close(self) -> None:
        """Release any resources held by the strategy."""
