from langgraph.graph import END, START, StateGraph

from agents.analyst_agent import analyst_node
from agents.research_agent import research_node
from agents.reviewer_agent import reviewer_node
from agents.supervisor import supervisor_node
from graph.routing import route_from_supervisor
from graph.state import CreditRiskState


def build_graph() -> StateGraph:
    graph = StateGraph(CreditRiskState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("research", research_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("reviewer", reviewer_node)

    graph.add_edge(START, "supervisor")
    graph.add_conditional_edges(
        "supervisor",
        route_from_supervisor,
        {
            "research": "research",
            "analyst": "analyst",
            "reviewer": "reviewer",
            "__end__": END,
        },
    )
    graph.add_edge("research", "supervisor")
    graph.add_edge("analyst", "supervisor")
    graph.add_edge("reviewer", "supervisor")
    return graph


def compile_graph():
    return build_graph().compile()
