from mcp.server.fastmcp import FastMCP

from tools.database_tools import search_loan_products
from tools.research_tools import credit_policy_retriever, document_retriever, web_search

mcp = FastMCP("credit-research")


@mcp.tool()
def web_search_tool(query: str, max_results: int = 5) -> list[dict]:
    """Search the web for lender criteria, rates, and eligibility context."""
    return web_search(query, max_results=max_results)


@mcp.tool()
def loan_product_search(
    product_type: str = "personal",
    amount: float = 0,
    tenure_months: int = 0,
    credit_score: int = 0,
) -> list[dict]:
    """Search internal loan product catalog by type, amount, tenure and score."""
    return search_loan_products(product_type, amount, tenure_months, credit_score)


@mcp.tool()
def document_retriever_tool(query: str, n_results: int = 5) -> list[dict]:
    """Retrieve policy and research documents from the vector store."""
    return document_retriever(query, n_results=n_results)


@mcp.tool()
def credit_policy_retriever_tool(query: str, limit: int = 5) -> list[dict]:
    """Fetch credit-policy excerpts relevant to the request."""
    return credit_policy_retriever(query, limit=limit)


if __name__ == "__main__":
    from mcp_servers.serve import run_mcp

    run_mcp(mcp, 8101)
