from flask import Blueprint, jsonify, render_template, request

from app.repositories import repos
from app.services import ai_service, trend_service

bp = Blueprint("trend", __name__, url_prefix="/trend")


def _postings():
    return repos().postings.list_postings(job_name=request.args.get("job_name") or None)


@bp.route("/")
def page():
    postings = _postings()
    job_name = request.args.get("job_name") or "전체"
    top = trend_service.top_keywords(postings, 10)
    return render_template(
        "trend.html",
        summary=ai_service.summarize_stats(job_name, top, len(postings)),
        job_names=[j for j, _ in trend_service.job_counts(repos().postings.list_postings())],
        job_name=request.args.get("job_name") or "",
    )


@bp.route("/api/keywords")
def api_keywords():
    n = request.args.get("n", 10, type=int)
    return jsonify([{"keyword": k, "count": c} for k, c in trend_service.top_keywords(_postings(), n)])


@bp.route("/api/weekly")
def api_weekly():
    n = request.args.get("n", 5, type=int)
    return jsonify(trend_service.weekly_keyword_trend(_postings(), n))


@bp.route("/api/regions")
def api_regions():
    return jsonify([{"label": k, "count": c} for k, c in trend_service.region_distribution(_postings())])


@bp.route("/api/experience")
def api_experience():
    return jsonify([{"label": k, "count": c} for k, c in trend_service.experience_distribution(_postings())])
