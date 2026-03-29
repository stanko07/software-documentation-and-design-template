"""SQLAlchemy implementation of ICityRepository."""

from typing import Optional

from sqlalchemy.orm import Session

from src.dal.interfaces.i_city_repository import ICityRepository
from src.models.orm_models import City


class CityRepository(ICityRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_name(self, name: str) -> Optional[City]:
        return self._session.query(City).filter_by(name=name).first()

    def get_or_create(self, name: str) -> City:
        city = self.get_by_name(name)
        if city is None:
            city = City(name=name)
            self._session.add(city)
            self._session.flush()
        return city
