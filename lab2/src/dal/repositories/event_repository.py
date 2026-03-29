"""SQLAlchemy implementation of IEventRepository."""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.dal.interfaces.i_event_repository import IEventRepository
from src.models.orm_models import Event


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
