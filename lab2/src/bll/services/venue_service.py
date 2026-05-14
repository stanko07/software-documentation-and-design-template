from typing import List, Optional

from src.dal.repositories.venue_repository import VenueRepository
from src.dal.repositories.city_repository import CityRepository
from src.models.orm_models import Venue


class VenueService:
    def __init__(self, venue_repo: VenueRepository, city_repo: CityRepository) -> None:
        self._venues = venue_repo
        self._cities = city_repo

    def list_venues(self) -> List[Venue]:
        return self._venues.get_all()

    def get_venue(self, venue_id: str) -> Optional[Venue]:
        return self._venues.get_by_id(venue_id)

    def create_venue(self, name: str, address: str, city_id: str) -> Venue:
        if not name.strip():
            raise ValueError("Venue name cannot be empty.")
        if not self._cities.get_by_id(city_id):
            raise ValueError("City not found.")
        return self._venues.create(name.strip(), address.strip(), city_id)

    def update_venue(self, venue_id: str, name: str, address: str, city_id: str) -> Venue:
        if not name.strip():
            raise ValueError("Venue name cannot be empty.")
        if not self._cities.get_by_id(city_id):
            raise ValueError("City not found.")
        venue = self._venues.update(venue_id, name.strip(), address.strip(), city_id)
        if venue is None:
            raise ValueError("Venue not found.")
        return venue

    def delete_venue(self, venue_id: str) -> None:
        if not self._venues.delete(venue_id):
            raise ValueError("Venue not found.")
