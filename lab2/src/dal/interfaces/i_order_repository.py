"""Interface for the Order repository (including OrderItem)."""

from abc import ABC, abstractmethod

from src.models.orm_models import Order, OrderItem


class IOrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        """Persist a new Order (with its items) and return the managed instance."""

    @abstractmethod
    def add_item(self, item: OrderItem) -> OrderItem:
        """Persist an OrderItem and return the managed instance."""
