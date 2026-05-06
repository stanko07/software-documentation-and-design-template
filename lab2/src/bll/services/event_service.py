from datetime import datetime
from typing import List, Optional

from src.dal.repositories.event_repository import EventRepository
from src.dal.repositories.venue_repository import VenueRepository
from src.models.orm_models import Event


class EventService:
    def __init__(self, event_repo: EventRepository, venue_repo: VenueRepository) -> None:
        self._events = event_repo
        self._venues = venue_repo

    def list_events(self) -> List[Event]:
        return self._events.get_all()

    def get_event(self, event_id: str) -> Optional[Event]:
        return self._events.get_by_id(event_id)

    def create_event(self, title: str, date_time: datetime, venue_id: str) -> Event:
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if not self._venues.get_by_id(venue_id):
            raise ValueError("Venue not found.")
        return self._events.create(title.strip(), date_time, venue_id)

    def update_event(self, event_id: str, title: str, date_time: datetime, venue_id: str) -> Event:
        if not title.strip():
            raise ValueError("Title cannot be empty.")
        if not self._venues.get_by_id(venue_id):
            raise ValueError("Venue not found.")
        event = self._events.update(event_id, title.strip(), date_time, venue_id)
        if event is None:
            raise ValueError("Event not found.")
        return event

    def delete_event(self, event_id: str) -> None:
        if not self._events.delete(event_id):
            raise ValueError("Event not found.")
