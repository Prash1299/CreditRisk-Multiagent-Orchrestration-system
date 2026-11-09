import argparse
import json

from dotenv import load_dotenv

from graph.pipeline import run_assessment


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Credit-risk multi-agent assessment")
    parser.add_argument(
        "--request",
        default=(
            "I earn ₹85,000 per month, have an existing EMI of ₹15,000, "
            "a credit score of 720, and want a personal loan of ₹8 lakh for 4 years."
        ),
    )
    parser.add_argument("--session-id", default="cli")
    parser.add_argument("--borrower-id", default=None)
    args = parser.parse_args()
    result = run_assessment(args.request, session_id=args.session_id, borrower_id=args.borrower_id)
    print(json.dumps(result.model_dump(), indent=2, default=str))


if __name__ == "__main__":
    main()
