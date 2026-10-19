import pytest

from app import create_app
from app.schema import Posting
from app.services import recommend_service, saramin_client, trend_service


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    return app.test_client()


@pytest.mark.parametrize("path", ["/", "/jobs/", "/jobs/90000001", "/trend/", "/mypage", "/bookmarks", "/login", "/stats/"])
def test_pages_ok(client, path):
    assert client.get(path).status_code == 200


def test_filter_and_pagination(client):
    assert client.get("/jobs/?page=2&field=IT").status_code == 200
    assert client.get("/jobs/?location=없는지역").status_code == 200


def test_trend_api(client):
    for p in ("keywords", "weekly", "regions", "experience"):
        assert client.get(f"/trend/api/{p}").status_code == 200


def test_missing_job_404(client):
    assert client.get("/jobs/nope").status_code == 404


def test_bookmark_and_prefs_flow(client):
    client.post("/bookmarks/90000001/add")
    assert "/jobs/90000001" in client.get("/bookmarks").get_data(as_text=True)
    client.post("/bookmarks/90000001/remove")
    assert "/jobs/90000001" not in client.get("/bookmarks").get_data(as_text=True)
    r = client.post("/mypage", data={"jobs": "백엔드 개발", "keywords": "Java"}, follow_redirects=True)
    assert r.status_code == 200
    assert client.get("/").status_code == 200


def test_recommend_reason():
    p = Posting("1", "t", "c", "IT", "백엔드 개발", "서울 강남구", keywords=["Java", "AWS"])
    score, reason = recommend_service.score_posting(p, {"jobs": ["백엔드 개발"], "keywords": ["java", "aws"]})
    assert "관심 직무 일치" in reason and "키워드 2개 일치" in reason and score > 0


def test_trend_service():
    p = [Posting("1", "t", "c", "IT", "j", "서울 강남구", posted_at="2026-10-01", keywords=["A"])]
    assert trend_service.top_keywords(p) == [("A", 1)]


def test_saramin_client_requires_key(monkeypatch):
    monkeypatch.setattr(saramin_client.Config, "SARAMIN_ACCESS_KEY", "")
    with pytest.raises(saramin_client.SaraminConfigError):
        saramin_client.fetch_postings("백엔드 개발")
