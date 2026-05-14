"""
Flask MVC web application for tickets.ua (Lab 3 extension of Lab 2).

Usage
-----
    python web_app.py
    # Opens at http://127.0.0.1:5000

The existing main.py (CSV import) is unchanged.
"""

from __future__ import annotations

import os

from flask import Flask, g, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.models.orm_models import Base
from src.dal.repositories.city_repository import CityRepository
from src.dal.repositories.venue_repository import VenueRepository
from src.dal.repositories.event_repository import EventRepository
from src.bll.services.city_service import CityService
from src.bll.services.venue_service import VenueService
from src.bll.services.event_service import EventService
from src.presentation.controllers.event_controller import bp as events_bp
from src.presentation.controllers.city_controller import bp as cities_bp
from src.presentation.controllers.venue_controller import bp as venues_bp

DB_URL = os.environ.get("DATABASE_URL", "sqlite:///data/tickets.db")


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")

    engine = create_engine(DB_URL, echo=False, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    SessionFactory = sessionmaker(bind=engine)

    @app.before_request
    def open_session() -> None:
        session: Session = SessionFactory()
        g.db_session = session

        city_repo  = CityRepository(session)
        venue_repo = VenueRepository(session)
        event_repo = EventRepository(session)

        g.city_service  = CityService(city_repo)
        g.venue_service = VenueService(venue_repo, city_repo)
        g.event_service = EventService(event_repo, venue_repo)

    @app.teardown_request
    def close_session(exc) -> None:
        session: Session | None = g.pop("db_session", None)
        if session:
            if exc:
                session.rollback()
            session.close()

    app.register_blueprint(events_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(venues_bp)

    @app.get("/")
    def index():
        return redirect(url_for("events.index"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
