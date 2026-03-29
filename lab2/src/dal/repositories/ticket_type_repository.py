"""SQLAlchemy implementation of ITicketTypeRepository."""

from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from src.dal.interfaces.i_ticket_type_repository import ITicketTypeRepository
from src.models.orm_models import TicketType


class TicketTypeRepository(ITicketTypeRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_name_and_event(self, name: str, event_id: str) -> Optional[TicketType]:
        return (
            self._session.query(TicketType)
            .filter_by(name=name, event_id=event_id)
            .first()
        )

    def get_or_create(
        self,
        name: str,
        price: Decimal,
        available_count: int,
        event_id: str,
    ) -> TicketType:
        tt = self.get_by_name_and_event(name, event_id)
        if tt is None:
            tt = TicketType(
                name=name,
                price=price,
                available_count=available_count,
                event_id=event_id,
            )
            self._session.add(tt)
            self._session.flush()
        return tt
