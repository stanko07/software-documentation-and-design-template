"""SQLAlchemy implementation of ICustomerRepository."""

from typing import Optional

from sqlalchemy.orm import Session

from src.dal.interfaces.i_customer_repository import ICustomerRepository
from src.models.orm_models import Customer


class CustomerRepository(ICustomerRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_email(self, email: str) -> Optional[Customer]:
        return self._session.query(Customer).filter_by(email=email).first()

    def get_or_create(self, full_name: str, email: str) -> Customer:
        customer = self.get_by_email(email)
        if customer is None:
            customer = Customer(full_name=full_name, email=email)
            self._session.add(customer)
            self._session.flush()
        return customer
