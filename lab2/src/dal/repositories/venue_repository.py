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

    def get_all(self) -> list:
        from sqlalchemy.orm import joinedload
        return (
            self._session.query(Venue)
            .options(joinedload(Venue.city))
            .order_by(Venue.name)
            .all()
        )

    def get_by_id(self, venue_id: str) -> Optional[Venue]:
        return self._session.query(Venue).filter_by(id=venue_id).first()

    def create(self, name: str, address: str, city_id: str) -> Venue:
        venue = Venue(name=name, address=address, city_id=city_id)
        self._session.add(venue)
        self._session.flush()
        return venue

    def update(self, venue_id: str, name: str, address: str, city_id: str) -> Optional[Venue]:
        venue = self.get_by_id(venue_id)
        if venue:
            venue.name = name
            venue.address = address
            venue.city_id = city_id
            self._session.flush()
        return venue

    def delete(self, venue_id: str) -> bool:
        venue = self.get_by_id(venue_id)
        if not venue:
            return False
        self._session.delete(venue)
        self._session.flush()
        return True
