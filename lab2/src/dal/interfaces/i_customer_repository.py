"""Interface for the Customer repository."""

from abc import ABC, abstractmethod
from typing import Optional

from src.models.orm_models import Customer


class ICustomerRepository(ABC):
    @abstractmethod
    def get_or_create(self, full_name: str, email: str) -> Customer:
        """Return existing customer by email or persist a new one."""

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Return customer by email, or None."""
