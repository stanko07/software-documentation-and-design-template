"""Interface for the Venue repository."""

from abc import ABC, abstractmethod
from typing import Optional

from src.models.orm_models import Venue


class IVenueRepository(ABC):
    @abstractmethod
    def get_or_create(self, name: str, address: str, city_id: str) -> Venue:
        """Return existing venue or persist a new one."""

    @abstractmethod
    def get_by_name_and_city(self, name: str, city_id: str) -> Optional[Venue]:
        """Return venue matching name + city, or None."""
