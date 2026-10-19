"""data/mock/*.json 및 세션/메모리 기반 구현체 (DB 도입 전까지 사용)."""
import json
import threading
from pathlib import Path

from flask import session

from app.repositories.base import PostingRepository, StatsRepository, UserRepository
from app.schema import Posting

MOCK_DIR = Path(__file__).resolve().parents[2] / "data" / "mock"


class MockPostingRepository(PostingRepository):
    def __init__(self, path=None):
        path = Path(path) if path else MOCK_DIR / "postings.json"
        with open(path, encoding="utf-8") as f:
            self._postings = [Posting.from_dict(d) for d in json.load(f)]
        self._postings.sort(key=lambda p: p.posted_at, reverse=True)

    def list_postings(self, field=None, job_name=None, location=None, experience=None):
        result = self._postings
        if field:
            result = [p for p in result if p.field == field]
        if job_name:
            result = [p for p in result if p.job_name == job_name]
        if location:
            result = [p for p in result if p.region == location]
        if experience:
            result = [p for p in result if experience in p.experience]
        return list(result)

    def get_posting(self, saramin_job_id):
        return next((p for p in self._postings if p.saramin_job_id == saramin_job_id), None)

    def list_recent(self, n=5):
        return self._postings[:n]


class SessionUserRepository(UserRepository):
    """Flask 세션에 저장. user_id는 무시 (DB 구현체에서 사용)."""

    def get_preferences(self, user_id):
        return dict(session.get("prefs", {}))

    def save_preferences(self, user_id, prefs):
        session["prefs"] = prefs

    def get_bookmarks(self, user_id):
        return list(session.get("bookmarks", []))

    def add_bookmark(self, user_id, saramin_job_id):
        marks = self.get_bookmarks(user_id)
        if saramin_job_id not in marks:
            marks.append(saramin_job_id)
        session["bookmarks"] = marks

    def remove_bookmark(self, user_id, saramin_job_id):
        session["bookmarks"] = [m for m in self.get_bookmarks(user_id) if m != saramin_job_id]


class MemoryStatsRepository(StatsRepository):
    def __init__(self):
        self._counts = {}
        self._lock = threading.Lock()

    def increment(self, page):
        with self._lock:
            self._counts[page] = self._counts.get(page, 0) + 1

    def get_all(self):
        with self._lock:
            return dict(self._counts)
