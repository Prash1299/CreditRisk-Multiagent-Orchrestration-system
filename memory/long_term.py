"""PostgreSQL + Chroma long-term memory facade."""

from memory.postgres_memory import save_interaction, search_interactions
from memory.retrieval import store_memory_vector


class LongTermMemory:
    def store(self, session_id: str, content: str, kind: str = "assessment") -> None:
        row = save_interaction(session_id, content, kind=kind)
        store_memory_vector(
            f"{session_id}-{row['id']}",
            content,
            {"session_id": session_id, "kind": kind},
        )

    def load(self, session_id: str) -> list[dict]:
        return search_interactions(session_id)
