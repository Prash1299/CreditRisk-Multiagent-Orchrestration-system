from models.risk_model import RiskModel
from tools.financial_tools import financial_calculator


def credit_risk_prediction(
    credit_score: float,
    monthly_income: float,
    existing_emi: float,
    loan_amount: float,
    tenure_months: int,
    annual_rate: float = 0.13,
    defaults: float = 0,
) -> dict:
    calcs = financial_calculator(
        monthly_income=monthly_income,
        existing_emi=existing_emi,
        loan_amount=loan_amount,
        tenure_months=tenure_months,
        annual_rate=annual_rate,
    )
    model = RiskModel.load()
    prediction = model.predict(
        {
            "credit_score": credit_score,
            "foir": calcs["foir"],
            "loan_to_income": calcs["loan_to_income"],
            "defaults": defaults,
        }
    )
    return {
        "probability_of_default": prediction.probability_of_default,
        "risk_band": prediction.risk_band,
        "application_score": _score(credit_score, calcs["foir"], prediction.probability_of_default),
        "inputs": calcs,
        "disclaimer": "Illustrative score only; not a regulated credit decision.",
    }


def _score(credit_score: float, foir: float, pd: float) -> float:
    credit_component = min(max((credit_score - 300) / 550 * 100, 0), 100)
    foir_component = max(0, 100 - foir * 140)
    pd_component = max(0, 100 - pd * 100)
    return round(0.4 * credit_component + 0.35 * foir_component + 0.25 * pd_component, 2)
