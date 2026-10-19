"""맞춤 추천 점수 + 추천 이유.

prefs 형식: {"jobs": [직무명], "location": 지역, "experience": 경력, "keywords": [키워드]}
"""


def score_posting(posting, prefs):
    """(score, reason_str) 반환."""
    score = 0
    parts = []
    if posting.job_name in prefs.get("jobs", []):
        score += 5
        parts.append("관심 직무 일치")
    if prefs.get("location") and posting.region == prefs["location"]:
        score += 2
        parts.append("선호 지역 일치")
    if prefs.get("experience") and prefs["experience"] in posting.experience:
        score += 2
        parts.append("경력 조건 일치")
    wanted = {k.lower() for k in prefs.get("keywords", [])}
    matched = [k for k in posting.keywords if k.lower() in wanted]
    if matched:
        score += len(matched)
        parts.append(f"키워드 {len(matched)}개 일치")
    return score, ", ".join(parts)


def recommend(postings, prefs, limit=10):
    """점수 > 0 인 공고를 [(posting, score, reason)] 로 점수 내림차순 반환."""
    scored = []
    for p in postings:
        s, r = score_posting(p, prefs)
        if s > 0:
            scored.append((p, s, r))
    scored.sort(key=lambda x: (x[1], x[0].posted_at), reverse=True)
    return scored[:limit]


def has_prefs(prefs):
    return any(prefs.get(k) for k in ("jobs", "location", "experience", "keywords"))
