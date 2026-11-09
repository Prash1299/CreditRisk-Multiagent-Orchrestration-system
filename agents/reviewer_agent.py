from tools.credit_tools import summarize_policy


def reviewer_node(state: dict) -> dict:
    analysis = state.get("analysis") or {}
    research = state.get("research") or {}
    score = float(state.get("risk_score") or analysis.get("application_score") or 0)
    policy = summarize_policy(research.get("policy_hits") or [])

    if score >= 70:
        recommendation = "approve"
    elif score >= 50:
        recommendation = "refer"
    else:
        recommendation = "decline"

    rationale = (
        f"Score {score:.1f} mapped to {recommendation}. "
        f"Risk band={analysis.get('risk_band')}. Policy: {policy}"
    )
    review = {
        "recommendation": recommendation,
        "rationale": rationale,
        "policy_summary": policy,
    }
    return {
        "review": review,
        "recommendation": recommendation,
        "rationale": rationale,
        "messages": [{"role": "assistant", "content": f"Reviewer: {rationale}"}],
    }
