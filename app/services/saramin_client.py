"""사람인 공식 API(https://oapi.saramin.co.kr/job-search) 클라이언트 뼈대.

크롤링 금지. 승인 전이므로 실제 호출 부분은 TODO. 중복 방지 기준은 saramin_job_id.
"""
import time
from datetime import date

from app.config import Config
from app.schema import Posting

API_URL = "https://oapi.saramin.co.kr/job-search"


class SaraminConfigError(RuntimeError):
    pass


class SaraminQuotaError(RuntimeError):
    pass


# 일일 호출 횟수 카운터 (프로세스 메모리. Lambda에서는 저장소로 옮길 것 - TODO)
_counter = {"day": None, "count": 0}
_last_call = {"t": 0.0}


def require_key():
    if not Config.SARAMIN_ACCESS_KEY:
        raise SaraminConfigError(
            "SARAMIN_ACCESS_KEY가 설정되지 않았습니다. .env에 키를 입력하거나 DATA_SOURCE=mock 으로 사용하세요."
        )
    return Config.SARAMIN_ACCESS_KEY


def _register_call():
    """한도 확인 + 호출 간 대기 + 카운터 증가."""
    today = date.today()
    if _counter["day"] != today:
        _counter.update(day=today, count=0)
    limit = Config.SARAMIN_DAILY_LIMIT  # TODO(승인 후 확인): 기본값 없음
    if limit is not None and _counter["count"] >= limit:
        raise SaraminQuotaError(f"일일 호출 한도({limit}) 초과")
    wait = Config.SARAMIN_CALL_INTERVAL_SEC - (time.monotonic() - _last_call["t"])
    if wait > 0:
        time.sleep(wait)
    _last_call["t"] = time.monotonic()
    _counter["count"] += 1


def calls_today():
    return _counter["count"] if _counter["day"] == date.today() else 0


def fetch_postings(job_name, start=0, count=10):
    """job_name 직무의 공고를 페이지 단위로 호출해 Posting 리스트로 반환."""
    key = require_key()
    _register_call()
    # TODO(승인 후 응답 확인): 실제 호출 구현.
    #   - 파라미터명(access-key, job_cd, start, count 등)과 직무 코드(config/jobs.py saramin_code) 확인
    #   - requests.get(API_URL, params={...}, headers={"Accept": "application/json"}, timeout=10)
    #   - 응답에서 공고 리스트를 꺼내 [normalize(item, job_name) for item in items]
    del key, start, count
    raise NotImplementedError("TODO(승인 후 응답 확인): 사람인 API 실제 호출 미구현")


def normalize(raw_item, field="", job_name=""):
    """API 원본 공고 1건 -> 내부 Posting. 응답 필드명 확정 전이라 매핑은 TODO."""
    # TODO(승인 후 응답 확인): 아래 매핑을 실제 응답 필드에 맞게 수정
    return Posting(
        saramin_job_id=str(raw_item.get("id", "")),  # TODO 매핑
        title=raw_item.get("title", ""),  # TODO 매핑
        company_name=raw_item.get("company", ""),  # TODO 매핑
        field=field,  # config/jobs.py 기준
        job_name=job_name,  # config/jobs.py 기준
        location=raw_item.get("location", ""),  # TODO 매핑
        lat=None,  # TODO: 좌표 제공 여부 확인 (Config.SARAMIN_PROVIDES_COORDS)
        lng=None,
        experience=raw_item.get("experience", ""),  # TODO 매핑
        education=raw_item.get("education", ""),  # TODO 매핑
        employment_type=raw_item.get("employment_type", ""),  # TODO 매핑
        salary=raw_item.get("salary", ""),  # TODO 매핑
        posted_at=raw_item.get("posted_at", ""),  # TODO 매핑 (YYYY-MM-DD로 변환)
        deadline_at=raw_item.get("deadline_at", ""),  # TODO 매핑 (YYYY-MM-DD로 변환)
        source_url=raw_item.get("url", ""),  # TODO 매핑
        keywords=list(raw_item.get("keywords", [])),  # TODO 매핑 (본문 없이 가능한 키워드만)
    )


def dedupe(postings, seen_ids=None):
    """saramin_job_id 기준 중복 제거. seen_ids(이미 저장된 id 집합)도 제외."""
    seen = set(seen_ids or ())
    result = []
    for p in postings:
        if p.saramin_job_id and p.saramin_job_id not in seen:
            seen.add(p.saramin_job_id)
            result.append(p)
    return result
