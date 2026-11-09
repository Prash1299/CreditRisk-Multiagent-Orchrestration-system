from __future__ import annotations

import csv
import sqlite3
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "credit_risk.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def get_connection() -> sqlite3.Connection:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@lru_cache(maxsize=1)
def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    _load_csv(
        conn,
        "borrowers",
        ROOT / "data" / "borrowers.csv",
        [
            "borrower_id",
            "name",
            "segment",
            "industry",
            "annual_income",
            "existing_debt",
            "collateral_value",
            "credit_score",
            "prior_defaults",
        ],
    )
    _load_csv(
        conn,
        "loan_products",
        ROOT / "data" / "loan_products.csv",
        ["product_id", "name", "amount", "term_months", "rate", "product_type"],
    )
    conn.commit()
    conn.close()


def _load_csv(conn: sqlite3.Connection, table: str, path: Path, columns: list[str]) -> None:
    if not path.exists():
        return
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    if count:
        return
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [tuple(row[col] for col in columns) for row in reader]
    placeholders = ", ".join("?" for _ in columns)
    col_sql = ", ".join(columns)
    conn.executemany(
        f"INSERT INTO {table} ({col_sql}) VALUES ({placeholders})",
        rows,
    )


def save_assessment(
    borrower_id: str,
    product_id: str,
    risk_score: float | None,
    recommendation: str | None,
    rationale: str | None,
) -> None:
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO assessments (borrower_id, product_id, risk_score, recommendation, rationale)
        VALUES (?, ?, ?, ?, ?)
        """,
        (borrower_id, product_id, risk_score, recommendation, rationale),
    )
    conn.commit()
    conn.close()
