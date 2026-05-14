"""
CSV generator module for Lab 2.

Generates a realistic dataset of at least 1000 rows compatible with the
tickets.ua domain model (City → Venue → Event → TicketType → Customer →
Order → OrderItem → Payment → Delivery).

Usage
-----
    python generate_csv.py                        # writes data/tickets_data.csv
    python generate_csv.py --rows 2000            # custom row count
    python generate_csv.py --output my_data.csv   # custom output path
"""

from __future__ import annotations

import argparse
import csv
import os
import random
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import NamedTuple

# ---------------------------------------------------------------------------
# Seed data pools
# ---------------------------------------------------------------------------

CITIES = [
    "Kyiv", "Lviv", "Odesa", "Kharkiv", "Dnipro",
    "Zaporizhzhia", "Vinnytsia", "Poltava", "Chernivtsi", "Mykolaiv",
]

VENUE_TEMPLATES = [
    ("{city} Opera House", "{city}, Teatralna St, 1"),
    ("{city} Palace of Sports", "{city}, Stadium Ave, 10"),
    ("{city} Philharmonic", "{city}, Svobody Sq, 3"),
    ("{city} Arena", "{city}, Olympic Blvd, 7"),
    ("{city} Cultural Center", "{city}, Culture St, 22"),
]

EVENT_TITLES = [
    "Rock Night Festival", "Jazz Evening", "Classical Gala",
    "Electronic Music Rave", "Stand-up Comedy Show", "Ballet Performance",
    "Opera Night", "Folk Music Concert", "Pop Stars Live", "Blues Session",
    "Hip-Hop Showcase", "Chamber Music Evening", "Symphony Orchestra",
    "World Music Festival", "New Year's Eve Special",
]

TICKET_TYPE_NAMES = ["Standard", "VIP", "Premium", "Economy", "Student"]

PAYMENT_PROVIDERS = ["LiqPay", "Fondy", "WayForPay", "Stripe", "PayPal"]

ORDER_STATUSES = ["created", "paid", "cancelled", "expired"]
PAYMENT_STATUSES = ["pending", "success", "failed"]
DELIVERY_STATUSES = ["sent", "failed"]

FIRST_NAMES = [
    "Olena", "Ivan", "Maria", "Andriy", "Natalia", "Dmytro", "Yulia",
    "Vasyl", "Iryna", "Serhiy", "Oksana", "Mykola", "Tetiana", "Roman",
    "Larysa", "Oleksandr", "Halyna", "Bohdan", "Svitlana", "Taras",
]
LAST_NAMES = [
    "Kovalenko", "Shevchenko", "Melnyk", "Bondarenko", "Kravchenko",
    "Tkachenko", "Savchenko", "Petrenko", "Kovalchuk", "Marchenko",
    "Moroz", "Lytvyn", "Karpenko", "Sydorenko", "Zaitsev",
    "Hrytsenko", "Pavlenko", "Rudenko", "Holub", "Lyashenko",
]


# ---------------------------------------------------------------------------
# Cached entities (to simulate realistic FK relationships)
# ---------------------------------------------------------------------------

class VenueRecord(NamedTuple):
    name: str
    address: str
    city: str


class EventRecord(NamedTuple):
    title: str
    date_time: datetime
    venue: VenueRecord


class TicketTypeRecord(NamedTuple):
    name: str
    price: Decimal
    available_count: int
    event: EventRecord


class CustomerRecord(NamedTuple):
    full_name: str
    email: str


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))


def _build_venues(count: int = 30) -> list[VenueRecord]:
    venues: list[VenueRecord] = []
    for city in CITIES:
        for name_tpl, addr_tpl in VENUE_TEMPLATES:
            venues.append(
                VenueRecord(
                    name=name_tpl.format(city=city),
                    address=addr_tpl.format(city=city),
                    city=city,
                )
            )
    return venues[:max(count, len(venues))]


def _build_events(venues: list[VenueRecord], count: int = 80) -> list[EventRecord]:
    events: list[EventRecord] = []
    now = datetime.now()
    for _ in range(count):
        venue = random.choice(venues)
        title = random.choice(EVENT_TITLES)
        dt = _random_date(now - timedelta(days=365), now + timedelta(days=365))
        events.append(EventRecord(title=title, date_time=dt, venue=venue))
    return events


def _build_ticket_types(events: list[EventRecord]) -> list[TicketTypeRecord]:
    tts: list[TicketTypeRecord] = []
    for event in events:
        for name in random.sample(TICKET_TYPE_NAMES, k=random.randint(1, 3)):
            price = Decimal(str(round(random.uniform(50, 2000), 2)))
            count = random.randint(10, 500)
            tts.append(TicketTypeRecord(
                name=name, price=price,
                available_count=count, event=event,
            ))
    return tts


def _build_customers(count: int = 200) -> list[CustomerRecord]:
    seen_emails: set[str] = set()
    customers: list[CustomerRecord] = []
    while len(customers) < count:
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        full_name = f"{fn} {ln}"
        email = f"{fn.lower()}.{ln.lower()}{random.randint(1, 9999)}@example.com"
        if email in seen_emails:
            continue
        seen_emails.add(email)
        customers.append(CustomerRecord(full_name=full_name, email=email))
    return customers


# ---------------------------------------------------------------------------
# CSV columns
# ---------------------------------------------------------------------------

FIELDNAMES = [
    "city_name",
    "venue_name",
    "venue_address",
    "event_title",
    "event_date_time",
    "ticket_type_name",
    "ticket_price",
    "ticket_available_count",
    "customer_full_name",
    "customer_email",
    "order_status",
    "order_created_at",
    "order_item_qty",
    "payment_status",
    "payment_provider",
    "payment_paid_at",
    "delivery_type",
    "delivery_status",
    "delivery_sent_at",
]


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate(output_path: str, rows: int = 1000) -> None:
    venues = _build_venues()
    events = _build_events(venues, count=max(80, rows // 15))
    ticket_types = _build_ticket_types(events)
    customers = _build_customers(count=max(200, rows // 5))

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    now = datetime.now()

    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()

        for _ in range(rows):
            tt = random.choice(ticket_types)
            event = tt.event
            venue = event.venue
            customer = random.choice(customers)

            order_status = random.choice(ORDER_STATUSES)
            order_created_at = _random_date(now - timedelta(days=180), now)

            qty = random.randint(1, 4)

            # Payment only for paid/cancelled orders
            has_payment = order_status in ("paid", "cancelled")
            payment_status = ""
            payment_provider = ""
            payment_paid_at = ""

            if has_payment:
                payment_status = "success" if order_status == "paid" else random.choice(["failed", "pending"])
                payment_provider = random.choice(PAYMENT_PROVIDERS)
                if payment_status == "success":
                    paid_dt = order_created_at + timedelta(minutes=random.randint(1, 20))
                    payment_paid_at = paid_dt.strftime("%Y-%m-%d %H:%M:%S")

            # Delivery only for paid orders
            has_delivery = order_status == "paid"
            delivery_type = ""
            delivery_status = ""
            delivery_sent_at = ""

            if has_delivery:
                delivery_type = "email"
                delivery_status = random.choice(DELIVERY_STATUSES)
                if delivery_status == "sent":
                    sent_dt = order_created_at + timedelta(minutes=random.randint(20, 60))
                    delivery_sent_at = sent_dt.strftime("%Y-%m-%d %H:%M:%S")

            writer.writerow({
                "city_name": venue.city,
                "venue_name": venue.name,
                "venue_address": venue.address,
                "event_title": event.title,
                "event_date_time": event.date_time.strftime("%Y-%m-%d %H:%M:%S"),
                "ticket_type_name": tt.name,
                "ticket_price": str(tt.price),
                "ticket_available_count": tt.available_count,
                "customer_full_name": customer.full_name,
                "customer_email": customer.email,
                "order_status": order_status,
                "order_created_at": order_created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "order_item_qty": qty,
                "payment_status": payment_status,
                "payment_provider": payment_provider,
                "payment_paid_at": payment_paid_at,
                "delivery_type": delivery_type,
                "delivery_status": delivery_status,
                "delivery_sent_at": delivery_sent_at,
            })

    print(f"Generated {rows} rows → {output_path}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a CSV data file for the tickets.ua domain model."
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=1000,
        help="Number of data rows to generate (default: 1000)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/tickets_data.csv",
        help="Output CSV file path (default: data/tickets_data.csv)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    generate(output_path=args.output, rows=args.rows)
