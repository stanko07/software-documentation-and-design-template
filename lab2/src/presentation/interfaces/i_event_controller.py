"""Presentation-layer interface for event-related operations."""

from abc import ABC, abstractmethod


class IEventController(ABC):
    """Placeholder for future event presentation logic."""

    @abstractmethod
    def list_events(self) -> None:
        """Display all available events."""

    @abstractmethod
    def get_event_details(self, event_id: str) -> None:
        """Display details of a single event."""
