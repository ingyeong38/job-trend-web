"""Repository 인터페이스. 추후 DB 구현체로 교체하면 된다."""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.schema import Posting


class PostingRepository(ABC):
    @abstractmethod
    def list_postings(self, field=None, job_name=None, location=None, experience=None) -> List[Posting]:
        """필터가 None이면 해당 조건 무시. 최신 게시일 순."""

    @abstractmethod
    def get_posting(self, saramin_job_id) -> Optional[Posting]: ...

    @abstractmethod
    def list_recent(self, n=5) -> List[Posting]: ...


class UserRepository(ABC):
    """사용자별 데이터(관심 설정, 북마크). 지금은 세션, 추후 DB."""

    @abstractmethod
    def get_preferences(self, user_id) -> dict: ...

    @abstractmethod
    def save_preferences(self, user_id, prefs: dict) -> None: ...

    @abstractmethod
    def get_bookmarks(self, user_id) -> List[str]: ...

    @abstractmethod
    def add_bookmark(self, user_id, saramin_job_id) -> None: ...

    @abstractmethod
    def remove_bookmark(self, user_id, saramin_job_id) -> None: ...


class StatsRepository(ABC):
    @abstractmethod
    def increment(self, page) -> None: ...

    @abstractmethod
    def get_all(self) -> dict: ...
