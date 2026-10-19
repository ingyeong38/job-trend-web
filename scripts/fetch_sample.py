"""승인 직후 응답 필드 확인용: job-search를 1회 호출해 원본을 data/raw/sample.json에 저장.

실행: python -m scripts.fetch_sample
"""
import json
import sys
from pathlib import Path

import requests

from app.config import Config
from app.services.saramin_client import API_URL

OUT = Path(__file__).resolve().parents[1] / "data" / "raw" / "sample.json"


def main():
    if not Config.SARAMIN_ACCESS_KEY:
        sys.exit("SARAMIN_ACCESS_KEY가 설정되지 않았습니다. .env를 확인하세요.")
    # TODO(승인 후 확인): 파라미터명 확인 (access-key, count 등)
    resp = requests.get(
        API_URL,
        params={"access-key": Config.SARAMIN_ACCESS_KEY, "count": 1},
        headers={"Accept": "application/json"},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("saved:", OUT)
    print("top-level keys:", list(data.keys()))
    # TODO: 공고 리스트 위치는 응답 구조 확인 후 수정 (아래는 흔한 구조를 가정한 탐색)
    item = _find_first_item(data)
    print("first item fields:", sorted(item.keys()) if item else "(공고 리스트를 찾지 못함 - sample.json 확인)")


def _find_first_item(node):
    if isinstance(node, list) and node and isinstance(node[0], dict):
        return node[0]
    if isinstance(node, dict):
        for v in node.values():
            found = _find_first_item(v)
            if found:
                return found
    return None


if __name__ == "__main__":
    main()
