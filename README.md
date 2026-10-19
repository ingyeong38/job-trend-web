# job-trend-web

사용자 맞춤 채용공고 추천과 채용공고 트렌드 분석을 제공하는 Flask 웹 앱 (클라우드 기반 웹 개발 수업 팀 프로젝트).

- 공고 수집은 크롤링 없이 **사람인 공식 API**만 사용합니다. 승인 전에는 `data/mock/postings.json` (가상 데이터 30건)으로 동작합니다.
- 사람인 API에는 공고 본문이 없다고 가정하므로 본문 분석 기능은 없습니다.
- 현재 DB는 없습니다. 사용자 설정·북마크는 세션, 방문 통계는 메모리에 저장됩니다 (`app/repositories/`만 교체하면 DB로 전환).

## 실행 방법 (macOS)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # 값 입력 (없어도 mock 모드로 동작)
python run.py            # http://127.0.0.1:5000
pytest                   # 테스트
```

## .env

`.env.example` 참고. 주요 값: `DATA_SOURCE`(mock|saramin, 기본 mock), `SARAMIN_ACCESS_KEY`, `GEMINI_API_KEY`(없으면 규칙 기반 문장으로 대체), `KAKAO_MAP_JS_KEY`(없으면 지도 대신 지역 텍스트), Google/카카오 OAuth 키, `FLASK_SECRET_KEY`. `.env`는 커밋하지 않습니다.

## 폴더 설명

| 경로 | 설명 |
|---|---|
| `app/__init__.py` | `create_app` (app factory), 방문 카운트, D-day 필터 |
| `app/config.py` | 환경변수 로딩, 사람인 관련 TODO 상수 |
| `app/schema.py` | 내부 공고 스키마 `Posting` (dataclass) |
| `app/blueprints/` | main, jobs, trend, auth, mypage(+북마크), stats |
| `app/services/` | saramin_client, trend_service, recommend_service, ai_service |
| `app/repositories/` | `base.py` 인터페이스, `mock_repo.py` (JSON/세션/메모리 구현체) |
| `app/templates/`, `app/static/` | 화면 |
| `collector/lambda_handler.py` | Lambda 수집 함수 뼈대 (배포는 나중) |
| `config/jobs.py` | 분야·직무 목록 (`saramin_code` 포함) |
| `data/mock/` | mock 데이터 |
| `scripts/fetch_sample.py` | 승인 후 응답 필드 확인용 (`python -m scripts.fetch_sample`) |
| `tests/` | pytest 스모크 테스트 |

## 역할별 담당 파일

- **주인경**: `collector/`, `app/services/saramin_client.py`, `trend_service.py`, `recommend_service.py`, `ai_service.py`, `app/blueprints/trend.py`
- **양해민**: `app/blueprints/main.py`, `jobs.py`, `mypage.py`, 템플릿 중 메인·목록·상세·북마크 (`index.html`, `jobs_list.html`, `job_detail.html`, `bookmarks.html`)
- **공동**: `app/blueprints/auth.py`, `app/templates/base.html`, `app/config.py`

## 사람인 API 승인 후 해야 할 일

- [ ] 1. `.env`에 `SARAMIN_ACCESS_KEY` 입력
- [ ] 2. `python -m scripts.fetch_sample` 실행 후 `data/raw/sample.json`으로 응답 필드 확인 (호출 한도, 좌표 제공 여부도 확인)
- [ ] 3. `app/services/saramin_client.py`의 `normalize` 매핑과 `fetch_postings` 실제 호출 구현 (TODO 표시된 곳)
- [ ] 4. `config/jobs.py`에 `saramin_code` 채우기 (+ TODO 직무 이름 채우기), `app/config.py` 호출 한도 상수 설정
- [ ] 5. `DATA_SOURCE=saramin`으로 변경 후 확인 (수집 결과 저장소가 없으므로 DB 도입 전에는 mock 저장소 사용)
