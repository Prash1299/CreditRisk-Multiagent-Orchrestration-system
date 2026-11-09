from tools.runtime import invoke


def research_node(state: dict) -> dict:
    applicant = state.get("applicant") or {}
    product_type = applicant.get("product_type") or "personal"
    amount = float(applicant.get("loan_amount") or 0)
    tenure = int(applicant.get("tenure_months") or 48)
    score = int(applicant.get("credit_score") or 0)
    query = (
        f"India {product_type} loan eligibility credit score {score} "
        f"amount {amount} tenure {tenure} months FOIR criteria"
    )

    products = invoke(
        "loan_product_search",
        product_type=product_type,
        amount=amount,
        tenure_months=tenure,
        credit_score=score,
    )
    policy = invoke("credit_policy_retriever", query=product_type)
    documents = invoke("document_retriever", query=query)
    web = invoke("web_search", query=query)

    research = {
        "products": products,
        "policy_hits": policy,
        "documents": documents,
        "web": web,
        "query": query,
    }
    return {
        "research": research,
        "messages": [
            {
                "role": "assistant",
                "content": f"Research: found {len(products)} products and {len(policy)} policy excerpts.",
            }
        ],
    }
