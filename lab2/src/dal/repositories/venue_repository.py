"""SQLAlchemy implementation of IVenueRepository."""

from typing import Optional

from sqlalchemy.orm import Session

from src.dal.interfaces.i_venue_repository import IVenueRepository
from src.models.orm_models import Venue


class VenueRepository(IVenueRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_name_and_city(self, name: str, city_id: str) -> Optional[Venue]:
        return (
            self._session.query(Venue)
            .filter_by(name=name, city_id=city_id)
            .first()
        )

    def get_or_create(self, name: str, address: str, city_id: str) -> Venue:
        venue = self.get_by_name_and_city(name, city_id)
        if venue is None:
            venue = Venue(name=name, address=address, city_id=city_id)
            self._session.add(venue)
            self._session.flush()
        return venue
