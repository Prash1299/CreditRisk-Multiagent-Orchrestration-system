from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import ROOT, get_settings
from database.models import Base

_engine: Engine | None = None
_SessionFactory: sessionmaker[Session] | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        settings = get_settings()
        connect_args = {}
        url = settings.database_url
        if url.startswith("sqlite"):
            (ROOT / "data").mkdir(parents=True, exist_ok=True)
            connect_args = {"check_same_thread": False}
        _engine = create_engine(url, future=True, connect_args=connect_args)
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = sessionmaker(bind=get_engine(), expire_on_commit=False)
    return _SessionFactory


@contextmanager
def session_scope() -> Iterator[Session]:
    factory = get_session_factory()
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    engine = get_engine()
    Base.metadata.create_all(engine)
    from database.seed import seed_if_empty

    seed_if_empty()


def run_select(sql: str) -> list[dict]:
    """Read-only SQL used by the analyst SQL tool."""
    stripped = sql.strip().rstrip(";")
    lowered = stripped.lower()
    if not lowered.startswith("select"):
        raise ValueError("Only SELECT queries are allowed")
    forbidden = (" insert ", " update ", " delete ", " drop ", " alter ", " pragma ")
    padded = f" {lowered} "
    if any(token in padded for token in forbidden):
        raise ValueError("Query contains a forbidden keyword")
    init_db()
    with get_engine().connect() as conn:
        rows = conn.execute(text(stripped)).mappings().all()
    return [dict(row) for row in rows]
