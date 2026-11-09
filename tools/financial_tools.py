from __future__ import annotations


def monthly_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    if principal <= 0 or tenure_months <= 0:
        return 0.0
    r = annual_rate / 12
    if r <= 0:
        return round(principal / tenure_months, 2)
    factor = (1 + r) ** tenure_months
    return round(principal * r * factor / (factor - 1), 2)


def foir(existing_emi: float, new_emi: float, monthly_income: float) -> float:
    if monthly_income <= 0:
        return 1.0
    return round((existing_emi + new_emi) / monthly_income, 4)


def loan_to_income(loan_amount: float, annual_income: float) -> float:
    if annual_income <= 0:
        return 1.0
    return round(loan_amount / annual_income, 4)


def compute_dti(total_annual_debt_service: float, annual_income: float) -> float:
    if annual_income <= 0:
        return 1.0
    return round(total_annual_debt_service / annual_income, 4)


def compute_ltv(loan_amount: float, collateral_value: float) -> float:
    if collateral_value <= 0:
        return 1.0
    return round(loan_amount / collateral_value, 4)


def financial_calculator(
    monthly_income: float,
    existing_emi: float,
    loan_amount: float,
    tenure_months: int,
    annual_rate: float = 0.13,
    annual_income: float | None = None,
) -> dict:
    emi = monthly_emi(loan_amount, annual_rate, tenure_months)
    income_annual = annual_income if annual_income else monthly_income * 12
    ratios = {
        "proposed_emi": emi,
        "foir": foir(existing_emi, emi, monthly_income),
        "existing_emi_ratio": round(existing_emi / monthly_income, 4) if monthly_income else 1.0,
        "loan_to_income": loan_to_income(loan_amount, income_annual),
        "dti": compute_dti((existing_emi + emi) * 12, income_annual),
        "surplus_after_emis": round(monthly_income - existing_emi - emi, 2),
        "assumptions": {
            "annual_rate": annual_rate,
            "tenure_months": tenure_months,
        },
    }
    return ratios
