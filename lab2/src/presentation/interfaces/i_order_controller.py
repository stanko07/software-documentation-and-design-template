"""Presentation-layer interface for order-related operations."""

from abc import ABC, abstractmethod


class IOrderController(ABC):
    """Placeholder for future order presentation logic."""

    @abstractmethod
    def create_order(self, customer_id: str, ticket_type_id: str, qty: int) -> None:
        """Handle an order creation request."""

    @abstractmethod
    def get_order_details(self, order_id: str) -> None:
        """Display the details of an order."""
