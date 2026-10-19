"""분야·직무 목록. saramin_code는 사람인 직무 코드 매핑용 (승인 후 채울 것)."""

FIELDS = [
    {
        "name": "IT",
        "jobs": [
            {"name": "백엔드 개발", "saramin_code": ""},
            {"name": "프론트엔드 개발", "saramin_code": ""},
            {"name": "데이터 분석", "saramin_code": ""},
            {"name": "정보보안", "saramin_code": ""},
        ],
    },
    {
        "name": "전기·전자",
        "jobs": [
            {"name": "회로 설계", "saramin_code": ""},
            {"name": "임베디드 SW", "saramin_code": ""},
            {"name": "반도체 공정", "saramin_code": ""},
            {"name": "전기 설계", "saramin_code": ""},
        ],
    },
    {
        "name": "디자인",
        "jobs": [
            {"name": "UI/UX 디자인", "saramin_code": ""},
            {"name": "웹 디자인", "saramin_code": ""},
            {"name": "그래픽 디자인", "saramin_code": ""},
            {"name": "영상 디자인", "saramin_code": ""},
        ],
    },
]


def field_names():
    return [f["name"] for f in FIELDS]


def all_jobs():
    """[(field, job_name, saramin_code), ...]"""
    return [(f["name"], j["name"], j["saramin_code"]) for f in FIELDS for j in f["jobs"]]


def jobs_of(field):
    for f in FIELDS:
        if f["name"] == field:
            return [j["name"] for j in f["jobs"]]
    return []
