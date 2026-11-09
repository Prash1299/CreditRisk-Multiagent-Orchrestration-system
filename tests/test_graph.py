from graph.workflow import compile_graph
from tools.financial_tools import compute_dti, compute_ltv


def test_ratios():
    assert compute_dti(25000, 100000) == 0.25
    assert compute_ltv(80, 100) == 0.8


def test_end_to_end_assessment():
    graph = compile_graph()
    result = graph.invoke(
        {
            "borrower_id": "B001",
            "product_id": "P200",
            "request": "Assess",
            "messages": [{"role": "user", "content": "Assess"}],
        }
    )
    assert result.get("research")
    assert result.get("analysis")
    assert result.get("review")
    assert result.get("recommendation") in {"approve", "refer", "decline"}
