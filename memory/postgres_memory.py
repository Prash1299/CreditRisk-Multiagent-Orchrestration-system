from sqlalchemy import select

from database.db import init_db, session_scope
from database.models import AssessmentRecord, InteractionMemory


def save_interaction(session_id: str, content: str, kind: str = "note") -> dict:
    init_db()
    with session_scope() as session:
        row = InteractionMemory(session_id=session_id, kind=kind, content=content)
        session.add(row)
        session.flush()
        return {"id": row.id, "session_id": session_id, "kind": kind}


def search_interactions(session_id: str, limit: int = 8) -> list[dict]:
    init_db()
    with session_scope() as session:
        rows = session.scalars(
            select(InteractionMemory)
            .where(InteractionMemory.session_id == session_id)
            .order_by(InteractionMemory.id.desc())
            .limit(limit)
        ).all()
    return [
        {
            "id": row.id,
            "session_id": row.session_id,
            "kind": row.kind,
            "content": row.content,
            "created_at": str(row.created_at) if row.created_at else None,
        }
        for row in reversed(rows)
    ]


def save_assessment_row(
    session_id: str,
    request: str,
    disposition: str | None,
    risk_score: float | None,
    rationale: str | None,
    payload_json: str | None,
) -> None:
    init_db()
    with session_scope() as session:
        session.add(
            AssessmentRecord(
                session_id=session_id,
                request=request,
                disposition=disposition,
                risk_score=risk_score,
                rationale=rationale,
                payload_json=payload_json,
            )
        )
