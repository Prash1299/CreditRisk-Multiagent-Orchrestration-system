from database.db import get_connection


def get_borrower(borrower_id: str) -> dict | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM borrowers WHERE borrower_id = ?", (borrower_id,)
    ).fetchone()
    return dict(row) if row else None


def get_loan_product(product_id: str) -> dict | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM loan_products WHERE product_id = ?", (product_id,)
    ).fetchone()
    return dict(row) if row else None


def list_borrowers(limit: int = 50) -> list[dict]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM borrowers ORDER BY borrower_id LIMIT ?", (limit,)
    ).fetchall()
    return [dict(row) for row in rows]
