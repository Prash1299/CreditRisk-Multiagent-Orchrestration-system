from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Borrower(Base):
    __tablename__ = "borrowers"

    borrower_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    segment: Mapped[str] = mapped_column(String(64), default="consumer")
    industry: Mapped[str] = mapped_column(String(64), default="general")
    monthly_income: Mapped[float] = mapped_column(Float, default=0)
    existing_emi: Mapped[float] = mapped_column(Float, default=0)
    collateral_value: Mapped[float] = mapped_column(Float, default=0)
    credit_score: Mapped[int] = mapped_column(Integer, default=0)
    prior_defaults: Mapped[int] = mapped_column(Integer, default=0)


class LoanProduct(Base):
    __tablename__ = "loan_products"

    product_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    lender: Mapped[str] = mapped_column(String(120))
    name: Mapped[str] = mapped_column(String(160))
    product_type: Mapped[str] = mapped_column(String(32), index=True)
    min_amount: Mapped[float] = mapped_column(Float)
    max_amount: Mapped[float] = mapped_column(Float)
    min_tenure_months: Mapped[int] = mapped_column(Integer)
    max_tenure_months: Mapped[int] = mapped_column(Integer)
    rate_from: Mapped[float] = mapped_column(Float)
    rate_to: Mapped[float] = mapped_column(Float)
    min_credit_score: Mapped[int] = mapped_column(Integer)
    max_foir: Mapped[float] = mapped_column(Float)
    processing_fee_pct: Mapped[float] = mapped_column(Float, default=1.0)
    notes: Mapped[str] = mapped_column(Text, default="")


class AssessmentRecord(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True)
    request: Mapped[str] = mapped_column(Text)
    disposition: Mapped[str | None] = mapped_column(String(32), nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    payload_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class InteractionMemory(Base):
    __tablename__ = "interaction_memory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(64), index=True)
    kind: Mapped[str] = mapped_column(String(32), default="note")
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
