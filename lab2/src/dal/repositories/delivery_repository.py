"""SQLAlchemy implementation of IDeliveryRepository."""

from sqlalchemy.orm import Session

from src.dal.interfaces.i_delivery_repository import IDeliveryRepository
from src.models.orm_models import Delivery


class DeliveryRepository(IDeliveryRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, delivery: Delivery) -> Delivery:
        self._session.add(delivery)
        self._session.flush()
        return delivery
