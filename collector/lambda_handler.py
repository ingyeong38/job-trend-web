"""Lambda 수집 함수 뼈대 (배포는 나중). saramin_client 재사용."""
from app.services import saramin_client
from config.jobs import all_jobs

PAGE_SIZE = 100  # TODO(승인 후 확인): API 최대 count


def handler(event=None, context=None):
    collected = []
    for field, job_name, _code in all_jobs():
        if job_name.startswith("TODO"):
            continue
        # TODO: 페이지 반복(start 증가) 종료 조건은 응답 확인 후 결정
        postings = saramin_client.fetch_postings(job_name, start=0, count=PAGE_SIZE)
        for p in postings:
            p.field = field
        collected.extend(postings)
    unique = saramin_client.dedupe(collected)  # TODO: 이미 저장된 id 집합 전달
    # TODO: 저장소(DB) 연결 후 unique 저장
    return {"collected": len(collected), "unique": len(unique)}
