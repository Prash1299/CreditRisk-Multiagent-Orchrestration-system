def compute_dti(total_debt: float, annual_income: float) -> float:
    if annual_income <= 0:
        return 1.0
    return round(total_debt / annual_income, 4)


def compute_ltv(loan_amount: float, collateral_value: float) -> float:
    if collateral_value <= 0:
        return 1.0
    return round(loan_amount / collateral_value, 4)


def parse_financials(payload: dict) -> dict:
    return {
        "annual_income": float(payload.get("annual_income", 0) or 0),
        "existing_debt": float(payload.get("existing_debt", 0) or 0),
        "collateral_value": float(payload.get("collateral_value", 0) or 0),
    }
