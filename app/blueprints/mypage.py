from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.repositories import repos
from app.services import recommend_service
from config.jobs import FIELDS, all_jobs

bp = Blueprint("mypage", __name__)


def _uid():
    return session.get("user", {}).get("id")


@bp.route("/mypage", methods=["GET", "POST"])
def mypage():
    users = repos().users
    if request.method == "POST":
        valid_jobs = {j for _, j, _ in all_jobs()}
        prefs = {
            "jobs": [j for j in request.form.getlist("jobs") if j in valid_jobs],
            "location": request.form.get("location", "").strip(),
            "experience": request.form.get("experience", "").strip(),
            "keywords": [k.strip() for k in request.form.get("keywords", "").split(",") if k.strip()],
        }
        users.save_preferences(_uid(), prefs)
        flash("저장했습니다.")
        return redirect(url_for("mypage.mypage"))

    prefs = users.get_preferences(_uid())
    postings = repos().postings.list_postings()
    recs = recommend_service.recommend(postings, prefs, 5) if recommend_service.has_prefs(prefs) else []
    return render_template(
        "mypage.html",
        prefs=prefs,
        fields=FIELDS,
        locations=sorted({p.region for p in postings}),
        recs=recs,
    )


@bp.route("/bookmarks")
def bookmarks():
    ids = repos().users.get_bookmarks(_uid())
    items = [p for p in (repos().postings.get_posting(i) for i in ids) if p]
    return render_template("bookmarks.html", items=items)


@bp.route("/bookmarks/<job_id>/add", methods=["POST"])
def add_bookmark(job_id):
    if repos().postings.get_posting(job_id):
        repos().users.add_bookmark(_uid(), job_id)
    return redirect(request.referrer or url_for("mypage.bookmarks"))


@bp.route("/bookmarks/<job_id>/remove", methods=["POST"])
def remove_bookmark(job_id):
    repos().users.remove_bookmark(_uid(), job_id)
    return redirect(request.referrer or url_for("mypage.bookmarks"))
