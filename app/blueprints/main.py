from flask import Blueprint, render_template, session

from app.repositories import repos
from app.services import ai_service, recommend_service, trend_service

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    postings = repos().postings.list_postings()
    top = trend_service.top_keywords(postings, 5)
    prefs = repos().users.get_preferences(session.get("user", {}).get("id"))
    recs = recommend_service.recommend(postings, prefs, 3) if recommend_service.has_prefs(prefs) else []
    return render_template(
        "index.html",
        top_keywords=top,
        job_counts=trend_service.job_counts(postings),
        recent=repos().postings.list_recent(5),
        summary=ai_service.summarize_stats("전체", top, len(postings)),
        recs=recs,
    )
