"""Gemini 호출 래퍼. 키가 없거나 실패하면 규칙 기반 문장으로 대체한다.

용도: 통계 요약, 추천 이유 문장 생성 (공고 본문 분석 아님).
"""
import requests

from app.config import Config

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


def _call_gemini(prompt):
    resp = requests.post(
        GEMINI_URL.format(model=Config.GEMINI_MODEL),
        headers={"x-goog-api-key": Config.GEMINI_API_KEY, "Content-Type": "application/json"},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


def _generate(prompt, fallback):
    if not Config.GEMINI_API_KEY:
        return fallback
    try:
        return _call_gemini(prompt) or fallback
    except Exception:  # 네트워크/쿼터/응답 형식 오류 모두 fallback
        return fallback


def summarize_stats(job_name, top_keywords, total):
    """top_keywords: [(keyword, count)]"""
    if not top_keywords:
        return f"{job_name} 공고 데이터가 아직 없습니다."
    names = ", ".join(f"{k}({c}건)" for k, c in top_keywords[:3])
    fallback = f"{job_name} 공고 {total}건 중 가장 많이 요구되는 기술은 {names}입니다."
    prompt = (
        f"다음 채용공고 통계를 한국어 2문장 이내로 요약해줘. 직무: {job_name}, 공고 수: {total}, "
        f"상위 키워드: {top_keywords[:5]}"
    )
    return _generate(prompt, fallback)


def recommend_sentence(posting, reason):
    """reason: recommend_service가 만든 규칙 기반 이유 문자열."""
    if not reason:
        return ""
    fallback = f"추천 이유: {reason}"
    prompt = (
        f"사용자에게 이 공고를 추천하는 이유를 한국어 한 문장으로 써줘. 공고: {posting.title}({posting.job_name}), "
        f"근거: {reason}. 근거에 없는 내용은 지어내지 마."
    )
    return _generate(prompt, fallback)
