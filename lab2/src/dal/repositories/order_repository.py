"""SQLAlchemy implementation of IOrderRepository."""

from sqlalchemy.orm import Session

from src.dal.interfaces.i_order_repository import IOrderRepository
from src.models.orm_models import Order, OrderItem


class OrderRepository(IOrderRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, order: Order) -> Order:
        self._session.add(order)
        self._session.flush()
        return order

    def add_item(self, item: OrderItem) -> OrderItem:
        self._session.add(item)
        self._session.flush()
        return item
