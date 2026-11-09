from core.constants import DISCLAIMER
from core.llm import complete


def reviewer_node(state: dict) -> dict:
    analysis = state.get("analysis") or {}
    research = state.get("research") or {}
    applicant = state.get("applicant") or {}
    recommendations = state.get("recommendations") or analysis.get("recommendations") or []
    calcs = analysis.get("calculator") or {}
    risk = analysis.get("risk") or {}
    issues = _checks(applicant, calcs, risk, recommendations, research)

    disposition = state.get("disposition") or "refer"
    if any(issue.startswith("blocking:") for issue in issues):
        disposition = "not_suitable"

    rationale = _rationale(applicant, calcs, risk, recommendations, disposition, issues)
    llm_text = complete(
        "You are a credit reviewer. Tighten the rationale. Keep it factual. "
        "Do not approve a loan. Decision-support only.",
        rationale,
    )
    if llm_text:
        rationale = llm_text

    review = {
        "issues": issues,
        "evidence": {
            "policy_sources": [hit.get("source") for hit in (research.get("policy_hits") or [])],
            "product_ids": [row.get("product_id") for row in recommendations],
            "python_emi_check": analysis.get("python_emi_check"),
        },
        "disposition": disposition,
        "rationale": rationale,
        "disclaimer": DISCLAIMER,
    }
    return {
        "review": review,
        "disposition": disposition,
        "rationale": rationale,
        "messages": [{"role": "assistant", "content": f"Reviewer: {disposition}. {rationale[:240]}"}],
    }


def _checks(applicant, calcs, risk, recommendations, research) -> list[str]:
    issues = []
    if not applicant.get("monthly_income") or not applicant.get("loan_amount"):
        issues.append("blocking: missing income or loan amount")
    if not recommendations:
        issues.append("blocking: no products in band")
    if not research.get("policy_hits"):
        issues.append("policy excerpts missing")
    foir = float(calcs.get("foir") or 0)
    if foir > 0.55:
        issues.append("blocking: FOIR above 55%")
    elif foir > 0.50:
        issues.append("FOIR in refer band (50-55%)")
    if int(applicant.get("credit_score") or 0) < 680:
        issues.append("score below unsecured policy floor")
    if analysis_mismatch(calcs, recommendations):
        issues.append("EMI/FOIR mismatch across products — using per-product calculator")
    return issues


def analysis_mismatch(calcs, recommendations) -> bool:
    if not recommendations:
        return False
    return abs(float(calcs.get("proposed_emi") or 0) - float(recommendations[0].get("proposed_emi") or 0)) > 1


def _rationale(applicant, calcs, risk, recommendations, disposition, issues) -> str:
    suitable = [row for row in recommendations if row["fit"] == "suitable"]
    refer = [row for row in recommendations if row["fit"] == "refer"]
    names = ", ".join(row["name"] for row in suitable[:3]) or "none"
    refer_names = ", ".join(row["name"] for row in refer[:3]) or "none"
    income = float(applicant.get("monthly_income") or 0)
    emi = float(applicant.get("existing_emi") or 0)
    amount = float(applicant.get("loan_amount") or 0)
    return (
        f"Applicant income ₹{income:,.0f}/month, existing EMI "
        f"₹{emi:,.0f}, score {applicant.get('credit_score')}, "
        f"request ₹{amount:,.0f} over {applicant.get('tenure_months')} months. "
        f"FOIR {float(calcs.get('foir') or 0):.1%}, illustrative PD {risk.get('probability_of_default')}, "
        f"band {risk.get('risk_band')}. Suitable options: {names}. Refer: {refer_names}. "
        f"Overall disposition: {disposition}. Issues: {'; '.join(issues) or 'none'}. "
        "This is decision support, not an approval."
    )
