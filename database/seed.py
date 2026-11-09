from pathlib import Path

from sqlalchemy import select

from database.db import session_scope
from database.models import Borrower, LoanProduct

PRODUCTS = [
    {
        "product_id": "PL-HDFC-01",
        "lender": "HDFC Bank",
        "name": "HDFC Personal Loan",
        "product_type": "personal",
        "min_amount": 50_000,
        "max_amount": 4_000_000,
        "min_tenure_months": 12,
        "max_tenure_months": 60,
        "rate_from": 0.105,
        "rate_to": 0.165,
        "min_credit_score": 700,
        "max_foir": 0.50,
        "processing_fee_pct": 1.5,
        "notes": "Salaried applicants; FOIR typically capped near 50%.",
    },
    {
        "product_id": "PL-SBI-01",
        "lender": "State Bank of India",
        "name": "SBI Xpress Credit",
        "product_type": "personal",
        "min_amount": 25_000,
        "max_amount": 2_000_000,
        "min_tenure_months": 12,
        "max_tenure_months": 72,
        "rate_from": 0.109,
        "rate_to": 0.155,
        "min_credit_score": 680,
        "max_foir": 0.50,
        "processing_fee_pct": 1.0,
        "notes": "Competitive rates for 700+ bureau scores.",
    },
    {
        "product_id": "PL-BAJ-01",
        "lender": "Bajaj Finance",
        "name": "Bajaj Flexi Personal Loan",
        "product_type": "personal",
        "min_amount": 100_000,
        "max_amount": 3_500_000,
        "min_tenure_months": 12,
        "max_tenure_months": 60,
        "rate_from": 0.11,
        "rate_to": 0.24,
        "min_credit_score": 685,
        "max_foir": 0.55,
        "processing_fee_pct": 2.0,
        "notes": "Faster turnaround; pricing sensitive to FOIR and score.",
    },
    {
        "product_id": "PL-ICICI-01",
        "lender": "ICICI Bank",
        "name": "ICICI Personal Loan",
        "product_type": "personal",
        "min_amount": 50_000,
        "max_amount": 5_000_000,
        "min_tenure_months": 12,
        "max_tenure_months": 60,
        "rate_from": 0.108,
        "rate_to": 0.16,
        "min_credit_score": 710,
        "max_foir": 0.48,
        "processing_fee_pct": 1.25,
        "notes": "Stricter FOIR for unsecured personal loans.",
    },
    {
        "product_id": "HL-SBI-01",
        "lender": "State Bank of India",
        "name": "SBI Home Loan",
        "product_type": "home",
        "min_amount": 500_000,
        "max_amount": 15_000_000,
        "min_tenure_months": 60,
        "max_tenure_months": 360,
        "rate_from": 0.082,
        "rate_to": 0.095,
        "min_credit_score": 700,
        "max_foir": 0.55,
        "processing_fee_pct": 0.35,
        "notes": "Secured; LTV and property documents required.",
    },
    {
        "product_id": "AL-HDFC-01",
        "lender": "HDFC Bank",
        "name": "HDFC Auto Loan",
        "product_type": "auto",
        "min_amount": 200_000,
        "max_amount": 2_500_000,
        "min_tenure_months": 12,
        "max_tenure_months": 84,
        "rate_from": 0.089,
        "rate_to": 0.12,
        "min_credit_score": 680,
        "max_foir": 0.55,
        "processing_fee_pct": 1.0,
        "notes": "Vehicle hypothecation required.",
    },
]

BORROWERS = [
    {
        "borrower_id": "B001",
        "name": "Amina Khan",
        "segment": "salaried",
        "industry": "it_services",
        "monthly_income": 85000,
        "existing_emi": 15000,
        "collateral_value": 0,
        "credit_score": 720,
        "prior_defaults": 0,
    },
    {
        "borrower_id": "B002",
        "name": "Luis Ortega",
        "segment": "salaried",
        "industry": "construction",
        "monthly_income": 54000,
        "existing_emi": 18000,
        "collateral_value": 160000,
        "credit_score": 661,
        "prior_defaults": 1,
    },
    {
        "borrower_id": "B003",
        "name": "Priya Shah",
        "segment": "self_employed",
        "industry": "retail",
        "monthly_income": 120000,
        "existing_emi": 22000,
        "collateral_value": 380000,
        "credit_score": 701,
        "prior_defaults": 0,
    },
]


def seed_if_empty() -> None:
    with session_scope() as session:
        has_products = session.scalar(select(LoanProduct.product_id).limit(1))
        if not has_products:
            session.add_all(LoanProduct(**row) for row in PRODUCTS)
        has_borrowers = session.scalar(select(Borrower.borrower_id).limit(1))
        if not has_borrowers:
            session.add_all(Borrower(**row) for row in BORROWERS)


def policy_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "credit_policy"
