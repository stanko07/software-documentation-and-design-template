"""SQLAlchemy implementation of IEventRepository."""

from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from src.dal.interfaces.i_event_repository import IEventRepository
from src.models.orm_models import Event, Venue


class EventRepository(IEventRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_title_and_venue(self, title: str, venue_id: str) -> Optional[Event]:
        return (
            self._session.query(Event)
            .filter_by(title=title, venue_id=venue_id)
            .first()
        )

    def get_or_create(self, title: str, date_time: datetime, venue_id: str) -> Event:
        event = self.get_by_title_and_venue(title, venue_id)
        if event is None:
            event = Event(title=title, date_time=date_time, venue_id=venue_id)
            self._session.add(event)
            self._session.flush()
        return event

    def get_all(self) -> list:
        from sqlalchemy.orm import joinedload
        return (
            self._session.query(Event)
            .options(joinedload(Event.venue).joinedload(Venue.city))
            .order_by(Event.date_time)
            .all()
        )

    def get_by_id(self, event_id: str) -> Optional[Event]:
        from sqlalchemy.orm import joinedload
        return (
            self._session.query(Event)
            .options(
                joinedload(Event.venue).joinedload(Venue.city),
                joinedload(Event.ticket_types),
            )
            .filter_by(id=event_id)
            .first()
        )

    def create(self, title: str, date_time: datetime, venue_id: str) -> Event:
        event = Event(title=title, date_time=date_time, venue_id=venue_id)
        self._session.add(event)
        self._session.flush()
        return event

    def update(self, event_id: str, title: str, date_time: datetime, venue_id: str) -> Optional[Event]:
        event = self._session.query(Event).filter_by(id=event_id).first()
        if event:
            event.title = title
            event.date_time = date_time
            event.venue_id = venue_id
            self._session.flush()
        return event

    def delete(self, event_id: str) -> bool:
        event = self._session.query(Event).filter_by(id=event_id).first()
        if not event:
            return False
        self._session.delete(event)
        self._session.flush()
        return True
