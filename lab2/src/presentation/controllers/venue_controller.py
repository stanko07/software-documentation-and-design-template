from flask import Blueprint, render_template, redirect, url_for, request, flash, g

bp = Blueprint("venues", __name__, url_prefix="/venues")


@bp.get("/")
def index():
    venues = g.venue_service.list_venues()
    return render_template("venues/index.html", venues=venues)


@bp.get("/new")
def new():
    cities = g.city_service.list_cities()
    return render_template("venues/form.html", venue=None, cities=cities)


@bp.post("/new")
def create():
    name = request.form.get("name", "").strip()
    address = request.form.get("address", "").strip()
    city_id = request.form.get("city_id", "")
    try:
        g.venue_service.create_venue(name, address, city_id)
        g.db_session.commit()
        flash("Venue created.", "success")
        return redirect(url_for("venues.index"))
    except ValueError as exc:
        g.db_session.rollback()
        flash(str(exc), "danger")
        cities = g.city_service.list_cities()
        return render_template("venues/form.html", venue=None, cities=cities), 422


@bp.get("/<venue_id>/edit")
def edit(venue_id: str):
    venue = g.venue_service.get_venue(venue_id)
    if venue is None:
        flash("Venue not found.", "danger")
        return redirect(url_for("venues.index"))
    cities = g.city_service.list_cities()
    return render_template("venues/form.html", venue=venue, cities=cities)


@bp.post("/<venue_id>/edit")
def update(venue_id: str):
    name = request.form.get("name", "").strip()
    address = request.form.get("address", "").strip()
    city_id = request.form.get("city_id", "")
    try:
        g.venue_service.update_venue(venue_id, name, address, city_id)
        g.db_session.commit()
        flash("Venue updated.", "success")
        return redirect(url_for("venues.index"))
    except ValueError as exc:
        g.db_session.rollback()
        flash(str(exc), "danger")
        cities = g.city_service.list_cities()
        venue = g.venue_service.get_venue(venue_id)
        return render_template("venues/form.html", venue=venue, cities=cities), 422


@bp.post("/<venue_id>/delete")
def delete(venue_id: str):
    try:
        g.venue_service.delete_venue(venue_id)
        g.db_session.commit()
        flash("Venue deleted.", "success")
    except ValueError as exc:
        g.db_session.rollback()
        flash(str(exc), "danger")
    return redirect(url_for("venues.index"))
