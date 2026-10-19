"""내부 공고 스키마 (공고 본문 필드 없음)."""
from dataclasses import asdict, dataclass, field, fields
from typing import List, Optional


@dataclass
class Posting:
    saramin_job_id: str
    title: str
    company_name: str
    field: str
    job_name: str
    location: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    experience: str = ""
    education: str = ""
    employment_type: str = ""
    salary: str = ""
    posted_at: str = ""  # YYYY-MM-DD
    deadline_at: str = ""  # YYYY-MM-DD
    source_url: str = ""
    keywords: List[str] = field(default_factory=list)

    @property
    def region(self):
        """'서울 강남구' -> '서울'"""
        return self.location.split()[0] if self.location else "기타"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        names = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in names})
