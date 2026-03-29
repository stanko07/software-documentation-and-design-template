"""Interface for reading raw data from a CSV file."""

from abc import ABC, abstractmethod
from typing import Iterator


class ICsvReader(ABC):
    """Reads rows from a CSV file and yields them as dicts."""

    @abstractmethod
    def read(self, file_path: str) -> Iterator[dict]:
        """Yield each row of the CSV as a dictionary keyed by column header."""
