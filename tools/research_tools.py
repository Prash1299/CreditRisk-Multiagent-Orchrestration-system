from pathlib import Path

from memory.retrieval import retrieve_similar_cases

POLICY_DIR = Path(__file__).resolve().parents[1] / "data" / "credit_policy"


def search_credit_policy(query: str, limit: int = 5) -> list[dict]:
    hits: list[dict] = []
    if not POLICY_DIR.exists():
        return hits
    needle = query.lower()
    for path in POLICY_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if needle in text.lower() or needle in path.stem.lower():
            hits.append({"source": path.name, "excerpt": text[:800]})
        if len(hits) >= limit:
            break
    if not hits:
        for path in list(POLICY_DIR.glob("*.md"))[:limit]:
            hits.append({"source": path.name, "excerpt": path.read_text(encoding="utf-8")[:800]})
    return hits


def search_market_notes(industry: str) -> list[dict]:
    return retrieve_similar_cases(industry)
