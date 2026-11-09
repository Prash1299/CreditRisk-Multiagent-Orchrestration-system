from tools.runtime import invoke


def analyst_node(state: dict) -> dict:
    applicant = state.get("applicant") or {}
    products = (state.get("research") or {}).get("products") or []
    monthly_income = float(applicant.get("monthly_income") or 0)
    existing_emi = float(applicant.get("existing_emi") or 0)
    loan_amount = float(applicant.get("loan_amount") or 0)
    tenure = int(applicant.get("tenure_months") or 48)
    score = float(applicant.get("credit_score") or 0)

    mid_rate = 0.13
    if products:
        mid_rate = float(products[0].get("rate_from") or 0.13)

    calcs = invoke(
        "financial_calculator",
        monthly_income=monthly_income,
        existing_emi=existing_emi,
        loan_amount=loan_amount,
        tenure_months=tenure,
        annual_rate=mid_rate,
    )
    emi_check = invoke(
        "python_code_execution",
        expression=f"round(emi({loan_amount}, {mid_rate}, {tenure}), 2)",
    )
    sql_rows = []
    try:
        product_type = applicant.get("product_type") or "personal"
        if product_type not in {"personal", "home", "auto", "sme"}:
            product_type = "personal"
        sql_rows = invoke(
            "sql_database_query",
            sql=(
                "SELECT product_id, lender, name, rate_from, max_amount, min_credit_score, max_foir "
                f"FROM loan_products WHERE product_type = '{product_type}'"
            ),
        )
    except Exception as exc:
        sql_rows = [{"error": str(exc)}]

    risk = invoke(
        "credit_risk_prediction",
        credit_score=score,
        monthly_income=monthly_income,
        existing_emi=existing_emi,
        loan_amount=loan_amount,
        tenure_months=tenure,
        annual_rate=mid_rate,
    )
    recommendations = _recommend(applicant, products, risk)

    analysis = {
        "calculator": calcs,
        "python_emi_check": emi_check,
        "sql_products": sql_rows,
        "risk": risk,
        "recommendations": recommendations,
    }
    overall = _overall(recommendations)
    return {
        "analysis": analysis,
        "recommendations": recommendations,
        "risk_score": risk.get("application_score"),
        "probability_of_default": risk.get("probability_of_default"),
        "disposition": overall,
        "messages": [
            {
                "role": "assistant",
                "content": (
                    f"Analyst: FOIR={calcs.get('foir')} PD={risk.get('probability_of_default')} "
                    f"score={risk.get('application_score')} options={len(recommendations)}"
                ),
            }
        ],
    }


def _recommend(applicant: dict, products: list[dict], risk: dict) -> list[dict]:
    monthly_income = float(applicant.get("monthly_income") or 0)
    existing_emi = float(applicant.get("existing_emi") or 0)
    loan_amount = float(applicant.get("loan_amount") or 0)
    tenure = int(applicant.get("tenure_months") or 48)
    score = int(applicant.get("credit_score") or 0)
    recs = []
    for product in products:
        rate = float(product.get("rate_from") or 0.13)
        calcs = invoke(
            "financial_calculator",
            monthly_income=monthly_income,
            existing_emi=existing_emi,
            loan_amount=loan_amount,
            tenure_months=tenure,
            annual_rate=rate,
        )
        reasons = []
        flags = []
        if score < int(product.get("min_credit_score") or 0):
            flags.append("credit_score_below_floor")
        if calcs["foir"] > float(product.get("max_foir") or 0.5) + 0.05:
            flags.append("foir_above_hard_cap")
        elif calcs["foir"] > float(product.get("max_foir") or 0.5):
            flags.append("foir_in_refer_band")
        if loan_amount < float(product.get("min_amount") or 0) or loan_amount > float(
            product.get("max_amount") or 0
        ):
            flags.append("amount_outside_product_band")
        if "foir_above_hard_cap" in flags or "amount_outside_product_band" in flags:
            fit = "not_suitable"
        elif flags:
            fit = "refer"
        else:
            fit = "suitable"
        if fit == "suitable":
            reasons.append(
                f"Score {score} meets {product.get('lender')} floor "
                f"and FOIR {calcs['foir']:.1%} is within {float(product.get('max_foir') or 0):.0%}."
            )
        else:
            reasons.append("; ".join(flags) or "See flags")
        recs.append(
            {
                "product_id": product.get("product_id"),
                "lender": product.get("lender"),
                "name": product.get("name"),
                "indicative_rate": rate,
                "proposed_emi": calcs["proposed_emi"],
                "foir": calcs["foir"],
                "fit": fit,
                "reasons": reasons,
                "risk_band": risk.get("risk_band"),
            }
        )
    recs.sort(key=lambda row: ({"suitable": 0, "refer": 1, "not_suitable": 2}[row["fit"]], row["foir"]))
    return recs


def _overall(recommendations: list[dict]) -> str:
    fits = {row["fit"] for row in recommendations}
    if "suitable" in fits:
        return "suitable"
    if "refer" in fits:
        return "refer"
    return "not_suitable"
