from sqlalchemy import select

from database.db import init_db, run_select, session_scope
from database.models import Borrower, LoanProduct


def get_borrower(borrower_id: str) -> dict | None:
    init_db()
    with session_scope() as session:
        row = session.get(Borrower, borrower_id)
        return _asdict(row) if row else None


def get_loan_product(product_id: str) -> dict | None:
    init_db()
    with session_scope() as session:
        row = session.get(LoanProduct, product_id)
        return _asdict(row) if row else None


def search_loan_products(
    product_type: str = "personal",
    amount: float = 0,
    tenure_months: int = 0,
    credit_score: int = 0,
    limit: int = 8,
) -> list[dict]:
    init_db()
    with session_scope() as session:
        stmt = select(LoanProduct)
        if product_type:
            stmt = stmt.where(LoanProduct.product_type == product_type)
        if amount:
            stmt = stmt.where(LoanProduct.min_amount <= amount, LoanProduct.max_amount >= amount)
        if tenure_months:
            stmt = stmt.where(
                LoanProduct.min_tenure_months <= tenure_months,
                LoanProduct.max_tenure_months >= tenure_months,
            )
        rows = session.scalars(stmt.limit(limit)).all()
        products = [_asdict(row) for row in rows]
    if credit_score:
        for product in products:
            product["meets_score_floor"] = credit_score >= int(product.get("min_credit_score") or 0)
    return products


def sql_database_query(sql: str) -> list[dict]:
    return run_select(sql)


def _asdict(row) -> dict:
    return {col.name: getattr(row, col.name) for col in row.__table__.columns}
