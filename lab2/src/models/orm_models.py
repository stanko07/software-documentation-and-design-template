"""SQLAlchemy ORM models matching the class diagram from Lab 1."""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Column, String, DateTime, Integer, Numeric, ForeignKey, Enum
)
from sqlalchemy.dialects.sqlite import CHAR
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


def _uuid() -> str:
    return str(uuid.uuid4())


class City(Base):
    __tablename__ = "cities"

    id = Column(CHAR(36), primary_key=True, default=_uuid)
    name = Column(String(100), nullable=False, unique=True)

    venues = relationship("Venue", back_populates="city")


class Venue(Base):
    __tablename__ = "venues"

    id = Column(CHAR(36), primary_key=True, default=_uuid)
    name = Column(String(200), nullable=False)
    address = Column(String(300), nullable=False)
    city_id = Column(CHAR(36), ForeignKey("cities.id"), nullable=False)

    city = relationship("City", back_populates="venues")
    events = relationship("Event", back_populates="venue")


class Event(Base):
    __tablename__ = "events"

    id = Column(CHAR(36), primary_key=True, default=_uuid)
    title = Column(String(200), nullable=False)
    date_time = Column(DateTime, nullable=False)
    venue_id = Column(CHAR(36), ForeignKey("venues.id"), nullable=False)

    venue = relationship("Venue", back_populates="events")
    ticket_types = relationship("TicketType", back_populates="event")


class TicketType(Base):
    __tablename__ = "ticket_types"

    id = Column(CHAR(36), primary_key=True, default=_uuid)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    available_count = Column(Integer, nullable=False)
    event_id = Column(CHAR(36), ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="ticket_types")
    order_items = relationship("OrderItem", back_populates="ticket_type")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(CHAR(36), primary_key=True, default=_uuid)
    full_name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)

    orders = relationship("Order", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(CHAR(36), primary_key=True, default=_uuid)
    status = Column(
        Enum("created", "paid", "cancelled", "expired", name="order_status"),
        nullable=False,
        default="created",
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    total = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    customer_id = Column(CHAR(36), ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", uselist=False, back_populates="order")
    delivery = relationship("Delivery", uselist=False, back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(CHAR(36), primary_key=True, default=_uuid)
    qty = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    order_id = Column(CHAR(36), ForeignKey("orders.id"), nullable=False)
    ticket_type_id = Column(CHAR(36), ForeignKey("ticket_types.id"), nullable=False)

    order = relationship("Order", back_populates="items")
    ticket_type = relationship("TicketType", back_populates="order_items")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(CHAR(36), primary_key=True, default=_uuid)
    status = Column(
        Enum("pending", "success", "failed", name="payment_status"),
        nullable=False,
        default="pending",
    )
    provider = Column(String(100), nullable=False)
    paid_at = Column(DateTime, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    order_id = Column(CHAR(36), ForeignKey("orders.id"), nullable=False, unique=True)

    order = relationship("Order", back_populates="payment")


class Delivery(Base):
    __tablename__ = "deliveries"

    id = Column(CHAR(36), primary_key=True, default=_uuid)
    type = Column(
        Enum("email", name="delivery_type"),
        nullable=False,
        default="email",
    )
    status = Column(
        Enum("sent", "failed", name="delivery_status"),
        nullable=False,
        default="sent",
    )
    sent_at = Column(DateTime, nullable=True)
    order_id = Column(CHAR(36), ForeignKey("orders.id"), nullable=False, unique=True)

    order = relationship("Order", back_populates="delivery")
