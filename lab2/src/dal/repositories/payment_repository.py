"""SQLAlchemy implementation of IPaymentRepository."""

from sqlalchemy.orm import Session

from src.dal.interfaces.i_payment_repository import IPaymentRepository
from src.models.orm_models import Payment


class PaymentRepository(IPaymentRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, payment: Payment) -> Payment:
        self._session.add(payment)
        self._session.flush()
        return payment
