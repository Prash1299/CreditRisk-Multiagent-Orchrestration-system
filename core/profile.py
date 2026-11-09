from __future__ import annotations

import re
from typing import Any

_Lakh = 100_000
_CRORE = 10_000_000


def parse_applicant(text: str) -> dict[str, Any]:
    """Extract income, EMI, score, amount and tenure from free-text requests."""
    raw = text or ""
    monthly_income = _first_amount(
        raw,
        [
            r"(?:earn|income|salary)[^\d₹rs]{0,24}(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lac|crore)?",
            r"(?:rs\.?|inr|₹)\s*([\d,]+(?:\.\d+)?)\s*(lakh|lac|crore)?[^\n]{0,20}(?:per month|/month|monthly)",
        ],
    )
    existing_emi = _first_amount(
        raw,
        [
            r"(?:existing\s+)?emi[^\d₹rs]{0,24}(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lac|crore)?",
        ],
    )
    loan_amount = _first_amount(
        raw,
        [
            r"(?:personal loan|loan|want)[^\d₹rs]{0,40}(?:rs\.?|inr|₹)?\s*([\d,]+(?:\.\d+)?)\s*(lakh|lac|crore)",
            r"(?:rs\.?|inr|₹)\s*([\d,]+(?:\.\d+)?)\s*(lakh|lac|crore)?[^\n]{0,24}(?:loan)",
        ],
    )
    credit_score = _first_int(raw, r"credit score[^\d]{0,12}(\d{3})")
    tenure_months = _tenure_months(raw)
    product_type = "personal"
    lowered = raw.lower()
    if "home" in lowered or "mortgage" in lowered:
        product_type = "home"
    elif "auto" in lowered or "car" in lowered:
        product_type = "auto"
    elif "business" in lowered or "sme" in lowered:
        product_type = "sme"

    annual_income = monthly_income * 12 if monthly_income else 0
    return {
        "raw_request": raw,
        "monthly_income": monthly_income,
        "annual_income": annual_income,
        "existing_emi": existing_emi,
        "loan_amount": loan_amount,
        "credit_score": credit_score,
        "tenure_months": tenure_months,
        "product_type": product_type,
        "currency": "INR",
    }


def _tenure_months(text: str) -> int:
    years = re.search(r"(\d+(?:\.\d+)?)\s*(?:years|year)", text, re.I)
    months = re.search(r"(\d+)\s*(?:months|month)", text, re.I)
    if years:
        return int(float(years.group(1)) * 12)
    if months:
        return int(months.group(1))
    return 48


def _first_int(text: str, pattern: str) -> int:
    match = re.search(pattern, text, re.I)
    return int(match.group(1)) if match else 0


def _first_amount(text: str, patterns: list[str]) -> float:
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if not match:
            continue
        number = float(match.group(1).replace(",", ""))
        unit = match.group(2).lower() if match.lastindex and match.group(2) else ""
        if unit in {"lakh", "lac"}:
            number *= _Lakh
        elif unit == "crore":
            number *= _CRORE
        return number
    return 0.0
