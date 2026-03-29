"""Interface for the City repository."""

from abc import ABC, abstractmethod
from typing import Optional

from src.models.orm_models import City


class ICityRepository(ABC):
    @abstractmethod
    def get_or_create(self, name: str) -> City:
        """Return existing city by name or persist a new one."""

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[City]:
        """Return city by name, or None if not found."""
