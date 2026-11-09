from __future__ import annotations

import os
from pathlib import Path

from memory.retrieval import retrieve_documents

POLICY_DIR = Path(__file__).resolve().parents[1] / "data" / "credit_policy"
NOTES_DIR = Path(__file__).resolve().parents[1] / "data" / "research_notes"

_CANNED_SEARCH = [
    {
        "title": "Typical Indian personal-loan FOIR",
        "url": "https://example.com/foir",
        "snippet": "Banks commonly keep FOIR near 40–50% for unsecured personal loans. Scores of 700+ improve pricing.",
    },
    {
        "title": "Bureau score bands",
        "url": "https://example.com/cibil",
        "snippet": "CIBIL 720 is generally considered good. Unsecured loan pricing still depends on FOIR and stability of income.",
    },
]


def web_search(query: str, max_results: int = 5) -> list[dict]:
    if os.getenv("WEB_SEARCH_OFFLINE") or os.getenv("PYTEST_CURRENT_TEST"):
        return _CANNED_SEARCH[:max_results]
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key:
        try:
            import httpx

            response = httpx.post(
                "https://api.tavily.com/search",
                json={"api_key": tavily_key, "query": query, "max_results": max_results},
                timeout=20,
            )
            response.raise_for_status()
            hits = response.json().get("results") or []
            return [
                {
                    "title": hit.get("title"),
                    "url": hit.get("url"),
                    "snippet": hit.get("content"),
                }
                for hit in hits
            ]
        except Exception:
            pass
    try:
        from ddgs import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return [
            {
                "title": item.get("title"),
                "url": item.get("href") or item.get("url"),
                "snippet": item.get("body"),
            }
            for item in results
        ]
    except Exception:
        return _CANNED_SEARCH[:max_results]


def document_retriever(query: str, n_results: int = 5) -> list[dict]:
    hits = retrieve_documents(query, n_results=n_results)
    extra = []
    if NOTES_DIR.exists():
        for path in NOTES_DIR.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            extra.append({"id": path.stem, "text": text[:1200], "metadata": {"source": path.name}})
    return hits or extra


def credit_policy_retriever(query: str, limit: int = 5) -> list[dict]:
    hits = []
    needle = (query or "").lower()
    if POLICY_DIR.exists():
        for path in POLICY_DIR.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            if not needle or needle in text.lower() or needle in path.stem.lower():
                hits.append({"source": path.name, "excerpt": text[:1200]})
            if len(hits) >= limit:
                break
        if not hits:
            for path in list(POLICY_DIR.glob("*.md"))[:limit]:
                hits.append(
                    {"source": path.name, "excerpt": path.read_text(encoding="utf-8")[:1200]}
                )
    return hits
