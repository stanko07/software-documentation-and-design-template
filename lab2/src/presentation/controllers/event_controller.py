from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash, g

from src.presentation.interfaces.i_event_controller import IEventController

bp = Blueprint("events", __name__, url_prefix="/events")


class EventController(IEventController):
    """Flask implementation of IEventController."""

    def list_events(self):
        events = g.event_service.list_events()
        return render_template("events/index.html", events=events)

    def get_event_details(self, event_id: str):
        event = g.event_service.get_event(event_id)
        if event is None:
            flash("Event not found.", "danger")
            return redirect(url_for("events.index"))
        return render_template("events/detail.html", event=event)


# ── Flask route wiring ────────────────────────────────────────────────────────

@bp.get("/")
def index():
    return EventController().list_events()


@bp.get("/<event_id>")
def detail(event_id: str):
    return EventController().get_event_details(event_id)


@bp.get("/new")
def new():
    venues = g.venue_service.list_venues()
    return render_template("events/form.html", event=None, venues=venues)


@bp.post("/new")
def create():
    title = request.form.get("title", "").strip()
    date_time_str = request.form.get("date_time", "")
    venue_id = request.form.get("venue_id", "")
    try:
        dt = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M")
        g.event_service.create_event(title, dt, venue_id)
        g.db_session.commit()
        flash("Event created.", "success")
        return redirect(url_for("events.index"))
    except (ValueError, Exception) as exc:
        g.db_session.rollback()
        flash(str(exc), "danger")
        venues = g.venue_service.list_venues()
        return render_template("events/form.html", event=None, venues=venues), 422


@bp.get("/<event_id>/edit")
def edit(event_id: str):
    event = g.event_service.get_event(event_id)
    if event is None:
        flash("Event not found.", "danger")
        return redirect(url_for("events.index"))
    venues = g.venue_service.list_venues()
    return render_template("events/form.html", event=event, venues=venues)


@bp.post("/<event_id>/edit")
def update(event_id: str):
    title = request.form.get("title", "").strip()
    date_time_str = request.form.get("date_time", "")
    venue_id = request.form.get("venue_id", "")
    try:
        dt = datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M")
        g.event_service.update_event(event_id, title, dt, venue_id)
        g.db_session.commit()
        flash("Event updated.", "success")
        return redirect(url_for("events.detail", event_id=event_id))
    except (ValueError, Exception) as exc:
        g.db_session.rollback()
        flash(str(exc), "danger")
        venues = g.venue_service.list_venues()
        event = g.event_service.get_event(event_id)
        return render_template("events/form.html", event=event, venues=venues), 422


@bp.post("/<event_id>/delete")
def delete(event_id: str):
    try:
        g.event_service.delete_event(event_id)
        g.db_session.commit()
        flash("Event deleted.", "success")
    except ValueError as exc:
        g.db_session.rollback()
        flash(str(exc), "danger")
    return redirect(url_for("events.index"))
