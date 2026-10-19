from flask import Blueprint, abort, current_app, render_template, request, session

from app.repositories import repos
from app.services import ai_service, recommend_service, trend_service
from config.jobs import FIELDS

bp = Blueprint("jobs", __name__, url_prefix="/jobs")

EXPERIENCE_OPTIONS = ["신입", "경력", "경력무관"]


@bp.route("/")
def list_jobs():
    f = {k: request.args.get(k) or None for k in ("field", "job_name", "location", "experience")}
    all_postings = repos().postings.list_postings()
    postings = repos().postings.list_postings(**f)

    per_page = current_app.config["PER_PAGE"]
    page = max(request.args.get("page", 1, type=int), 1)
    total_pages = max((len(postings) + per_page - 1) // per_page, 1)
    page = min(page, total_pages)
    items = postings[(page - 1) * per_page : page * per_page]

    # 페이지 링크용 쿼리 (page 제외)
    query = {k: v for k, v in f.items() if v}
    return render_template(
        "jobs_list.html",
        items=items,
        total=len(postings),
        page=page,
        total_pages=total_pages,
        filters=f,
        query=query,
        fields=FIELDS,
        locations=sorted({p.region for p in all_postings}),
        experience_options=EXPERIENCE_OPTIONS,
    )


@bp.route("/<job_id>")
def detail(job_id):
    posting = repos().postings.get_posting(job_id)
    if posting is None:
        abort(404)
    all_postings = repos().postings.list_postings()
    ranking = trend_service.keyword_ranking_for_job(all_postings, posting.job_name)
    rank_of = {k: (r, c) for r, k, c in ranking}

    user_id = session.get("user", {}).get("id")
    prefs = repos().users.get_preferences(user_id)
    _, reason = recommend_service.score_posting(posting, prefs)
    rec_line = ai_service.recommend_sentence(posting, reason)

    others = [p for p in all_postings if p.job_name == posting.job_name and p.saramin_job_id != job_id][:5]
    return render_template(
        "job_detail.html",
        p=posting,
        ranking=ranking[:10],
        tag_ranks=[(k, rank_of.get(k)) for k in posting.keywords],
        rec_line=rec_line,
        others=others,
        bookmarked=job_id in repos().users.get_bookmarks(user_id),
        kakao_key=current_app.config["KAKAO_MAP_JS_KEY"],
    )
