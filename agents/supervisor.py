from core.llm import complete
from core.profile import parse_applicant
from graph.state import CreditRiskState
from tools.runtime import invoke

PLAN = [
    {"agent": "research", "goal": "Gather products, policy and market context"},
    {"agent": "analyst", "goal": "Calculate ratios, PD and product fit"},
    {"agent": "reviewer", "goal": "Validate evidence and write the recommendation"},
]


def supervisor_node(state: CreditRiskState) -> dict:
    session_id = state.get("session_id") or "default"
    request = state.get("request") or ""
    updates: dict = {}

    if not state.get("applicant"):
        updates["applicant"] = parse_applicant(request)
        if state.get("borrower_id"):
            borrower = _safe_borrower(state["borrower_id"])
            if borrower:
                updates["applicant"] = {**updates["applicant"], **_from_borrower(borrower)}

    if state.get("prior_memory") is None:
        updates["prior_memory"] = invoke("memory_search", session_id=session_id, query=request, limit=5)

    if not state.get("execution_plan"):
        updates["execution_plan"] = _plan(request)

    if not state.get("research"):
        return {
            **updates,
            "next_agent": "research",
            "messages": [{"role": "assistant", "content": "Supervisor: delegating to Research Agent."}],
        }
    if not state.get("analysis"):
        return {
            **updates,
            "next_agent": "analyst",
            "messages": [{"role": "assistant", "content": "Supervisor: delegating to Data Analyst Agent."}],
        }
    if not state.get("review"):
        return {
            **updates,
            "next_agent": "reviewer",
            "messages": [{"role": "assistant", "content": "Supervisor: delegating to Reviewer Agent."}],
        }

    summary = (
        f"Disposition={state.get('disposition')} score={state.get('risk_score')} "
        f"request={request[:180]}"
    )
    invoke("memory_save", session_id=session_id, content=summary, kind="assessment")
    return {
        **updates,
        "next_agent": "__end__",
        "messages": [
            {
                "role": "assistant",
                "content": f"Supervisor: complete. {summary}",
            }
        ],
    }


def _plan(request: str) -> list[dict]:
    drafted = complete(
        "You are a credit-risk supervisor. Return a 3-step plan as plain text.",
        request,
    )
    if drafted:
        return [{"agent": "custom", "goal": drafted}, *PLAN]
    return PLAN


def _safe_borrower(borrower_id: str) -> dict | None:
    try:
        from tools.database_tools import get_borrower

        return get_borrower(borrower_id)
    except Exception:
        return None


def _from_borrower(borrower: dict) -> dict:
    monthly = float(borrower.get("monthly_income") or 0)
    return {
        "monthly_income": monthly,
        "annual_income": monthly * 12,
        "existing_emi": float(borrower.get("existing_emi") or 0),
        "credit_score": int(borrower.get("credit_score") or 0),
        "name": borrower.get("name"),
        "borrower_id": borrower.get("borrower_id"),
    }
