from mcp.server.fastmcp import FastMCP

from tools.research_tools import search_credit_policy, search_market_notes

mcp = FastMCP("credit-research")


@mcp.tool()
def policy_search(query: str) -> list[dict]:
    return search_credit_policy(query)


@mcp.tool()
def market_search(industry: str) -> list[dict]:
    return search_market_notes(industry)


if __name__ == "__main__":
    mcp.run()
