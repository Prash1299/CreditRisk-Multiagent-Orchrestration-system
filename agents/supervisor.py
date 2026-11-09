from graph.state import CreditRiskState


def supervisor_node(state: CreditRiskState) -> dict:
    """Route work among research, analyst, and reviewer, then stop."""
    if not state.get("research"):
        return {
            "next_agent": "research",
            "messages": [
                {"role": "assistant", "content": "Supervisor: sending case to research."}
            ],
        }
    if not state.get("analysis"):
        return {
            "next_agent": "analyst",
            "messages": [
                {"role": "assistant", "content": "Supervisor: sending case to analyst."}
            ],
        }
    if not state.get("review"):
        return {
            "next_agent": "reviewer",
            "messages": [
                {"role": "assistant", "content": "Supervisor: sending case to reviewer."}
            ],
        }
    return {
        "next_agent": "__end__",
        "messages": [
            {
                "role": "assistant",
                "content": (
                    f"Supervisor: complete. Recommendation={state.get('recommendation')} "
                    f"score={state.get('risk_score')}"
                ),
            }
        ],
    }
