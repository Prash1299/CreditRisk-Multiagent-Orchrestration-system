from pathlib import Path

from memory.chroma_store import query, upsert

POLICY_COLLECTION = "credit_policy"
MEMORY_COLLECTION = "session_memory"


def index_policy_docs(policy_dir: Path) -> int:
    count = 0
    for path in policy_dir.glob("*.md"):
        upsert(
            POLICY_COLLECTION,
            path.stem,
            path.read_text(encoding="utf-8"),
            {"source": path.name, "kind": "policy"},
        )
        count += 1
    return count


def retrieve_documents(query_text: str, n_results: int = 5) -> list[dict]:
    policy_dir = Path(__file__).resolve().parents[1] / "data" / "credit_policy"
    if policy_dir.exists():
        index_policy_docs(policy_dir)
    return query(POLICY_COLLECTION, query_text, n_results=n_results)


def retrieve_memory(query_text: str, n_results: int = 5) -> list[dict]:
    return query(MEMORY_COLLECTION, query_text, n_results=n_results)


def store_memory_vector(doc_id: str, text: str, metadata: dict | None = None) -> None:
    upsert(MEMORY_COLLECTION, doc_id, text, metadata)
