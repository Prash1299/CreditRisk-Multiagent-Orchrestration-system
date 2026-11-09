from typing import Annotated, Any, Literal

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

AgentName = Literal["supervisor", "research", "analyst", "reviewer"]

class CreditRiskState(TypedDict, total=False):
    """Shared state that flows through the multi-agent graph."""

    # Conversation context
    messages: Annotated[list, add_messages]
    request: str

    # Borrower and loan context
    borrower_id: str
    product_id: str

    # Agent outputs
    research: dict[str, Any]
    analysis: dict[str, Any]
    review: dict[str, Any]

    # Supervisor orchestration
    execution_plan: list[dict[str, Any]]
    next_agent: AgentName | Literal["__end__"]

    # Final assessment
    risk_score: float
    recommendation: Literal["approve", "refer", "decline"]
    rationale: str

    # Error handling and observability
    errors: list[str]

