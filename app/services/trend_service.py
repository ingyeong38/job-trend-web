"""키워드·직무·지역·경력 집계."""
from collections import Counter
from datetime import date


def _week_label(posted_at):
    y, w, _ = date.fromisoformat(posted_at).isocalendar()
    return f"{y}-W{w:02d}"


def top_keywords(postings, n=10):
    c = Counter(k for p in postings for k in p.keywords)
    return c.most_common(n)


def job_counts(postings):
    return Counter(p.job_name for p in postings).most_common()


def region_distribution(postings):
    return Counter(p.region for p in postings).most_common()


def experience_distribution(postings):
    return Counter(p.experience or "미정" for p in postings).most_common()


def weekly_keyword_trend(postings, n=5):
    """상위 n개 키워드의 주차별 공고 수. {'weeks': [...], 'series': {kw: [..]}}"""
    tops = [k for k, _ in top_keywords(postings, n)]
    weeks = sorted({_week_label(p.posted_at) for p in postings if p.posted_at})
    series = {k: [0] * len(weeks) for k in tops}
    for p in postings:
        if not p.posted_at:
            continue
        i = weeks.index(_week_label(p.posted_at))
        for k in p.keywords:
            if k in series:
                series[k][i] += 1
    return {"weeks": weeks, "series": series}


def keyword_ranking_for_job(postings, job_name):
    """같은 직무 내 키워드 인기 순위: [(rank, keyword, count)]"""
    same = [p for p in postings if p.job_name == job_name]
    return [(i + 1, k, c) for i, (k, c) in enumerate(top_keywords(same, 100))]
