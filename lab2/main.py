"""
Application entry point.

Wires all three layers together via Dependency Injection and runs the
CSV-to-database import.

Usage
-----
    python main.py                              # uses data/tickets_data.csv
    python main.py --csv path/to/file.csv       # custom CSV path
    python main.py --db sqlite:///mydb.db       # custom DB URL

Output strategy is controlled by config.json:
    { "output": { "strategy": "console" } }   <- default
    { "output": { "strategy": "kafka"   } }   <- switch to Kafka (no code change)
"""

from __future__ import annotations

import argparse
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ── Models (schema) ─────────────────────────────────────────────────────────
from src.models.orm_models import Base

# ── DAL implementations ──────────────────────────────────────────────────────
from src.dal.repositories.csv_reader import CsvReader
from src.dal.repositories.city_repository import CityRepository
from src.dal.repositories.venue_repository import VenueRepository
from src.dal.repositories.event_repository import EventRepository
from src.dal.repositories.ticket_type_repository import TicketTypeRepository
from src.dal.repositories.customer_repository import CustomerRepository
from src.dal.repositories.order_repository import OrderRepository
from src.dal.repositories.payment_repository import PaymentRepository
from src.dal.repositories.delivery_repository import DeliveryRepository

# ── BLL service ───────────────────────────────────────────────────────────────
from src.bll.services.import_service import ImportService

# ── Output strategy (Lab 4) ───────────────────────────────────────────────────
from src.output.strategy_factory import create_strategy
from src.output.output_context import OutputContext


def build_engine(db_url: str):
    return create_engine(db_url, echo=False)


def run_import(csv_path: str, db_url: str) -> None:
    engine = build_engine(db_url)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # OutputContext + strategy selected from config.json
    with OutputContext(create_strategy()) as out:
        try:
            csv_reader = CsvReader()
            city_repo         = CityRepository(session)
            venue_repo        = VenueRepository(session)
            event_repo        = EventRepository(session)
            ticket_type_repo  = TicketTypeRepository(session)
            customer_repo     = CustomerRepository(session)
            order_repo        = OrderRepository(session)
            payment_repo      = PaymentRepository(session)
            delivery_repo     = DeliveryRepository(session)

            import_service = ImportService(
                csv_reader=csv_reader,
                city_repo=city_repo,
                venue_repo=venue_repo,
                event_repo=event_repo,
                ticket_type_repo=ticket_type_repo,
                customer_repo=customer_repo,
                order_repo=order_repo,
                payment_repo=payment_repo,
                delivery_repo=delivery_repo,
            )

            out.write(f"Importing from: {csv_path}")
            out.write(f"Database:       {db_url}")

            count = import_service.import_from_csv(csv_path)
            session.commit()

            out.write(f"Successfully imported {count} rows.")

        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import tickets.ua CSV data into the database."
    )
    parser.add_argument(
        "--csv",
        default="data/tickets_data.csv",
        help="Path to the CSV file (default: data/tickets_data.csv)",
    )
    parser.add_argument(
        "--db",
        default="sqlite:///data/tickets.db",
        help="SQLAlchemy database URL (default: sqlite:///data/tickets.db)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    os.makedirs("data", exist_ok=True)
    run_import(csv_path=args.csv, db_url=args.db)
