from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

from core.config import get_settings

_client = None
_embed = DefaultEmbeddingFunction()


def get_client():
    global _client
    if _client is None:
        path = Path(get_settings().chroma_path)
        path.mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(path=str(path))
    return _client


def collection(name: str):
    return get_client().get_or_create_collection(name=name, embedding_function=_embed)


def upsert(name: str, doc_id: str, text: str, metadata: dict | None = None) -> None:
    collection(name).upsert(
        ids=[doc_id],
        documents=[text],
        metadatas=[metadata or {}],
    )


def query(name: str, text: str, n_results: int = 5) -> list[dict]:
    result = collection(name).query(query_texts=[text], n_results=n_results)
    docs = result.get("documents") or [[]]
    metas = result.get("metadatas") or [[]]
    ids = result.get("ids") or [[]]
    distances = result.get("distances") or [[]]
    hits = []
    for idx, doc in enumerate(docs[0]):
        hits.append(
            {
                "id": ids[0][idx] if ids[0] else str(idx),
                "text": doc,
                "metadata": metas[0][idx] if metas[0] else {},
                "distance": distances[0][idx] if distances[0] else None,
            }
        )
    return hits
