from tools.database_tools import get_borrower, get_loan_product
from tools.research_tools import search_credit_policy, search_market_notes


def research_node(state: dict) -> dict:
    borrower_id = state.get("borrower_id", "")
    product_id = state.get("product_id", "")
    borrower = get_borrower(borrower_id)
    product = get_loan_product(product_id)
    policy = search_credit_policy(borrower.get("segment", "consumer") if borrower else "consumer")
    market = search_market_notes(borrower.get("industry", "general") if borrower else "general")

    research = {
        "borrower": borrower,
        "product": product,
        "policy_hits": policy,
        "market_notes": market,
    }
    return {
        "research": research,
        "messages": [
            {
                "role": "assistant",
                "content": f"Research complete for borrower {borrower_id}.",
            }
        ],
    }
