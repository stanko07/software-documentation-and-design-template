"""Interface for the Event repository."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from src.models.orm_models import Event


class IEventRepository(ABC):
    @abstractmethod
    def get_or_create(self, title: str, date_time: datetime, venue_id: str) -> Event:
        """Return existing event or persist a new one."""

    @abstractmethod
    def get_by_title_and_venue(self, title: str, venue_id: str) -> Optional[Event]:
        """Return event matching title + venue, or None."""
