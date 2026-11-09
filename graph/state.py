from typing import Annotated, Any, Literal

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

AgentName = Literal["supervisor", "research", "analyst", "reviewer"]
Disposition = Literal["suitable", "refer", "not_suitable"]


class CreditRiskState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    request: str
    session_id: str
    borrower_id: str
    applicant: dict[str, Any]
    prior_memory: list[Any]
    execution_plan: list[dict[str, Any]]
    next_agent: AgentName | Literal["__end__"]
    research: dict[str, Any]
    analysis: dict[str, Any]
    review: dict[str, Any]
    recommendations: list[dict[str, Any]]
    risk_score: float
    probability_of_default: float
    disposition: Disposition
    rationale: str
    errors: list[str]
