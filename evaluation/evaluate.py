import json
from pathlib import Path

from graph.workflow import compile_graph

CASES_PATH = Path(__file__).with_name("test_cases.json")


def run() -> int:
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    graph = compile_graph()
    failures = 0
    for case in cases:
        result = graph.invoke(
            {
                "borrower_id": case["borrower_id"],
                "product_id": case["product_id"],
                "request": "Evaluate this application.",
                "messages": [{"role": "user", "content": "Evaluate this application."}],
            }
        )
        rec = result.get("recommendation")
        expected = case["expected_recommendation"]
        ok = rec in expected
        print(
            f"{case['id']}: recommendation={rec} expected={expected} "
            f"score={result.get('risk_score')} {'PASS' if ok else 'FAIL'}"
        )
        if not ok:
            failures += 1
    return failures


if __name__ == "__main__":
    raise SystemExit(run())
