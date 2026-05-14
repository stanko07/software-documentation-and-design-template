"""Interface for the Payment repository."""

from abc import ABC, abstractmethod

from src.models.orm_models import Payment


class IPaymentRepository(ABC):
    @abstractmethod
    def save(self, payment: Payment) -> Payment:
        """Persist a Payment record and return the managed instance."""
