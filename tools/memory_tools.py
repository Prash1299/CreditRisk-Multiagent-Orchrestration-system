from memory.long_term import LongTermMemory
from memory.postgres_memory import search_interactions
from memory.retrieval import retrieve_memory

_memory = LongTermMemory()


def memory_save(session_id: str, content: str, kind: str = "note") -> dict:
    _memory.store(session_id, content, kind=kind)
    return {"saved": True, "session_id": session_id, "kind": kind}


def memory_search(session_id: str, query: str = "", limit: int = 5) -> list[dict]:
    rows = search_interactions(session_id, limit=limit)
    if query:
        vector_hits = retrieve_memory(query, n_results=limit)
        return {"postgres": rows, "chroma": vector_hits}
    return rows
