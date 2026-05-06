from typing import List, Optional

from src.dal.repositories.city_repository import CityRepository
from src.models.orm_models import City


class CityService:
    def __init__(self, city_repo: CityRepository) -> None:
        self._cities = city_repo

    def list_cities(self) -> List[City]:
        return self._cities.get_all()

    def get_city(self, city_id: str) -> Optional[City]:
        return self._cities.get_by_id(city_id)

    def create_city(self, name: str) -> City:
        if not name.strip():
            raise ValueError("City name cannot be empty.")
        return self._cities.create(name.strip())

    def update_city(self, city_id: str, name: str) -> City:
        if not name.strip():
            raise ValueError("City name cannot be empty.")
        city = self._cities.update(city_id, name.strip())
        if city is None:
            raise ValueError("City not found.")
        return city

    def delete_city(self, city_id: str) -> None:
        if not self._cities.delete(city_id):
            raise ValueError("City not found.")
