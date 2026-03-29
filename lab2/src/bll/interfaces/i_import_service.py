"""BLL interface for the data-import service."""

from abc import ABC, abstractmethod


class IImportService(ABC):
    """Orchestrates reading a CSV file and persisting all entities to the DB."""

    @abstractmethod
    def import_from_csv(self, file_path: str) -> int:
        """
        Read *file_path*, build domain models, and save them to the database.

        Returns the number of rows successfully imported.
        """
