from flask import Blueprint, render_template, redirect, url_for, request, flash, g

bp = Blueprint("cities", __name__, url_prefix="/cities")


@bp.get("/")
def index():
    cities = g.city_service.list_cities()
    return render_template("cities/index.html", cities=cities)


@bp.get("/new")
def new():
    return render_template("cities/form.html", city=None)


@bp.post("/new")
def create():
    name = request.form.get("name", "").strip()
    try:
        g.city_service.create_city(name)
        g.db_session.commit()
        flash("City created.", "success")
        return redirect(url_for("cities.index"))
    except ValueError as exc:
        g.db_session.rollback()
        flash(str(exc), "danger")
        return render_template("cities/form.html", city=None), 422


@bp.get("/<city_id>/edit")
def edit(city_id: str):
    city = g.city_service.get_city(city_id)
    if city is None:
        flash("City not found.", "danger")
        return redirect(url_for("cities.index"))
    return render_template("cities/form.html", city=city)


@bp.post("/<city_id>/edit")
def update(city_id: str):
    name = request.form.get("name", "").strip()
    try:
        g.city_service.update_city(city_id, name)
        g.db_session.commit()
        flash("City updated.", "success")
        return redirect(url_for("cities.index"))
    except ValueError as exc:
        g.db_session.rollback()
        flash(str(exc), "danger")
        city = g.city_service.get_city(city_id)
        return render_template("cities/form.html", city=city), 422


@bp.post("/<city_id>/delete")
def delete(city_id: str):
    try:
        g.city_service.delete_city(city_id)
        g.db_session.commit()
        flash("City deleted.", "success")
    except ValueError as exc:
        g.db_session.rollback()
        flash(str(exc), "danger")
    return redirect(url_for("cities.index"))
