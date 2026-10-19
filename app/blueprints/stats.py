from flask import Blueprint, render_template

from app.repositories import repos

bp = Blueprint("stats", __name__, url_prefix="/stats")


@bp.route("/")
def visits():
    counts = sorted(repos().stats.get_all().items(), key=lambda x: -x[1])
    return render_template("stats.html", counts=counts)
