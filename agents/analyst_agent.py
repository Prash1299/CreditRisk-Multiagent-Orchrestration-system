from models.risk_model import RiskModel
from tools.credit_tools import score_application
from tools.financial_tools import compute_dti, compute_ltv


def analyst_node(state: dict) -> dict:
    research = state.get("research") or {}
    borrower = research.get("borrower") or {}
    product = research.get("product") or {}

    income = float(borrower.get("annual_income", 0) or 0)
    debt = float(borrower.get("existing_debt", 0) or 0)
    loan_amount = float(product.get("amount", 0) or 0)
    collateral = float(borrower.get("collateral_value", 0) or 0)

    dti = compute_dti(debt + loan_amount, income)
    ltv = compute_ltv(loan_amount, collateral)
    model = RiskModel.load()
    prediction = model.predict(
        {
            "credit_score": float(borrower.get("credit_score", 0) or 0),
            "dti": dti,
            "ltv": ltv,
            "defaults": float(borrower.get("prior_defaults", 0) or 0),
        }
    )
    application_score = score_application(
        credit_score=float(borrower.get("credit_score", 0) or 0),
        dti=dti,
        ltv=ltv,
        pd=prediction.probability_of_default,
    )

    analysis = {
        "dti": dti,
        "ltv": ltv,
        "model_pd": prediction.probability_of_default,
        "application_score": application_score,
        "risk_band": prediction.risk_band,
    }
    return {
        "analysis": analysis,
        "risk_score": application_score,
        "messages": [
            {
                "role": "assistant",
                "content": (
                    f"Analyst: DTI={dti:.2f} LTV={ltv:.2f} "
                    f"PD={prediction.probability_of_default:.3f} score={application_score:.1f}"
                ),
            }
        ],
    }
