from memory.long_term import LongTermMemory

_DEFAULT_NOTES = [
    {
        "industry": "retail",
        "note": "Consumer retail demand is stable; watch inventory-funded working capital.",
    },
    {
        "industry": "construction",
        "note": "Construction credit is cyclical; require stronger collateral coverage.",
    },
    {
        "industry": "general",
        "note": "Apply standard consumer policy unless a specialist overlay exists.",
    },
]


def retrieve_similar_cases(query: str, limit: int = 3) -> list[dict]:
    query_l = (query or "").lower()
    stored = LongTermMemory().load()
    corpus = stored + _DEFAULT_NOTES
    scored = []
    for item in corpus:
        hay = " ".join(str(v) for v in item.values()).lower()
        score = hay.count(query_l) if query_l else 0
        scored.append((score, item))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    hits = [item for score, item in scored if score > 0][:limit]
    if hits:
        return hits
    return _DEFAULT_NOTES[:limit]
