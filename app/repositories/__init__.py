from types import SimpleNamespace

from flask import current_app

from app.repositories.mock_repo import MemoryStatsRepository, MockPostingRepository, SessionUserRepository


def build_repos(config):
    """DATA_SOURCE에 따라 구현체 선택. DB 도입 시 여기만 교체."""
    # TODO: DB 구현체 추가 시 분기. 현재는 saramin 모드여도 mock 저장소 사용(수집 결과 저장소가 없음)
    return SimpleNamespace(
        postings=MockPostingRepository(),
        users=SessionUserRepository(),
        stats=MemoryStatsRepository(),
    )


def repos():
    return current_app.extensions["repos"]
