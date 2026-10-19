"""환경변수 로딩. 비밀키는 코드에 넣지 말고 .env에만 둔다."""
import os

from dotenv import load_dotenv

load_dotenv()


def _int_or_none(value):
    try:
        return int(value) if value not in (None, "") else None
    except ValueError:
        return None


class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY") or "dev-only-change-me"
    DATA_SOURCE = os.getenv("DATA_SOURCE", "mock")  # mock | saramin

    SARAMIN_ACCESS_KEY = os.getenv("SARAMIN_ACCESS_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    KAKAO_MAP_JS_KEY = os.getenv("KAKAO_MAP_JS_KEY", "")

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
    KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID", "")
    KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET", "")

    PER_PAGE = 10

    # ---- 사람인 API: 승인 후 확인 전이라 TODO 상수로 분리 ----
    # TODO(승인 후 확인): 일일 호출 한도. None이면 제한 없음으로 동작(위험하니 반드시 채울 것)
    SARAMIN_DAILY_LIMIT = _int_or_none(os.getenv("SARAMIN_DAILY_LIMIT"))
    # TODO(승인 후 확인): 호출 간 대기(초)
    SARAMIN_CALL_INTERVAL_SEC = float(os.getenv("SARAMIN_CALL_INTERVAL_SEC", "1.0"))
    # TODO(승인 후 확인): 근무지 좌표(lat/lng)를 API가 제공하는지 여부. None=미확인
    SARAMIN_PROVIDES_COORDS = None
    # TODO(승인 후 확인): 직무 코드는 config/jobs.py 의 saramin_code 에 입력
