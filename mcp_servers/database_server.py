from mcp.server.fastmcp import FastMCP

from tools.database_tools import get_borrower, get_loan_product, list_borrowers

mcp = FastMCP("credit-database")


@mcp.tool()
def borrower(borrower_id: str) -> dict | None:
    return get_borrower(borrower_id)


@mcp.tool()
def product(product_id: str) -> dict | None:
    return get_loan_product(product_id)


@mcp.tool()
def borrowers(limit: int = 50) -> list[dict]:
    return list_borrowers(limit)


if __name__ == "__main__":
    mcp.run()
