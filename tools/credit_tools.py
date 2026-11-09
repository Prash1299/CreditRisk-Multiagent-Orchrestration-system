def score_application(credit_score: float, dti: float, ltv: float, pd: float) -> float:
    credit_component = min(max((credit_score - 300) / 550 * 100, 0), 100)
    dti_component = max(0, 100 - dti * 100)
    ltv_component = max(0, 100 - ltv * 80)
    pd_component = max(0, 100 - pd * 100)
    return round(
        0.35 * credit_component
        + 0.25 * dti_component
        + 0.20 * ltv_component
        + 0.20 * pd_component,
        2,
    )


def summarize_policy(policy_hits: list[dict]) -> str:
    if not policy_hits:
        return "No matching policy documents found; apply default consumer limits."
    names = ", ".join(hit.get("source", "unknown") for hit in policy_hits[:3])
    return f"Reviewed policy sources: {names}."
