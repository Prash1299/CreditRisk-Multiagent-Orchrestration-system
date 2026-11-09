import argparse
import json

from dotenv import load_dotenv

from database.db import init_db, save_assessment
from graph.workflow import compile_graph
from memory.long_term import LongTermMemory


def run_assessment(borrower_id: str, product_id: str, request: str) -> dict:
    load_dotenv()
    init_db()
    graph = compile_graph()
    result = graph.invoke(
        {
            "borrower_id": borrower_id,
            "product_id": product_id,
            "request": request,
            "messages": [{"role": "user", "content": request}],
        }
    )
    save_assessment(
        borrower_id,
        product_id,
        result.get("risk_score"),
        result.get("recommendation"),
        result.get("rationale"),
    )
    LongTermMemory().store(
        {
            "borrower_id": borrower_id,
            "product_id": product_id,
            "recommendation": result.get("recommendation"),
            "risk_score": result.get("risk_score"),
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a credit-risk multi-agent assessment")
    parser.add_argument("--borrower-id", default="B001")
    parser.add_argument("--product-id", default="P200")
    parser.add_argument("--request", default="Assess this credit application.")
    args = parser.parse_args()
    result = run_assessment(args.borrower_id, args.product_id, args.request)
    printable = {
        "borrower_id": args.borrower_id,
        "product_id": args.product_id,
        "risk_score": result.get("risk_score"),
        "recommendation": result.get("recommendation"),
        "rationale": result.get("rationale"),
        "analysis": result.get("analysis"),
        "review": result.get("review"),
    }
    print(json.dumps(printable, indent=2, default=str))


if __name__ == "__main__":
    main()
