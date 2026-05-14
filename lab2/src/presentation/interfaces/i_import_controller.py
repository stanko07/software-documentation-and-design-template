"""Presentation-layer interface for the import controller."""

from abc import ABC, abstractmethod


class IImportController(ABC):
    """
    Entry point for the presentation layer.

    At this stage the presentation layer contains no logic and is
    represented only by this interface.
    """

    @abstractmethod
    def handle_import(self, file_path: str) -> None:
        """Trigger the CSV import and display the result to the user."""
