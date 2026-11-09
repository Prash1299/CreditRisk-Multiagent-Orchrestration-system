from typing import Literal

from graph.state import CreditRiskState


def route_from_supervisor(
    state: CreditRiskState,
) -> Literal["research", "analyst", "reviewer", "__end__"]:
    nxt = state.get("next_agent", "__end__")
    if nxt in {"research", "analyst", "reviewer", "__end__"}:
        return nxt
    return "__end__"
