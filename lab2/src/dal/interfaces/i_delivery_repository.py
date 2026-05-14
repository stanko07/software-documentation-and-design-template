"""Interface for the Delivery repository."""

from abc import ABC, abstractmethod

from src.models.orm_models import Delivery


class IDeliveryRepository(ABC):
    @abstractmethod
    def save(self, delivery: Delivery) -> Delivery:
        """Persist a Delivery record and return the managed instance."""
