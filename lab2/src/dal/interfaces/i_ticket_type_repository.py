"""Interface for the TicketType repository."""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional

from src.models.orm_models import TicketType


class ITicketTypeRepository(ABC):
    @abstractmethod
    def get_or_create(
        self,
        name: str,
        price: Decimal,
        available_count: int,
        event_id: str,
    ) -> TicketType:
        """Return existing ticket type or persist a new one."""

    @abstractmethod
    def get_by_name_and_event(self, name: str, event_id: str) -> Optional[TicketType]:
        """Return ticket type matching name + event, or None."""
