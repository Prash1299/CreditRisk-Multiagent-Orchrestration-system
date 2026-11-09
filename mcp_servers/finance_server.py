from mcp.server.fastmcp import FastMCP

from tools.credit_tools import score_application
from tools.financial_tools import compute_dti, compute_ltv

mcp = FastMCP("credit-finance")


@mcp.tool()
def dti(total_debt: float, annual_income: float) -> float:
    return compute_dti(total_debt, annual_income)


@mcp.tool()
def ltv(loan_amount: float, collateral_value: float) -> float:
    return compute_ltv(loan_amount, collateral_value)


@mcp.tool()
def application_score(credit_score: float, dti: float, ltv: float, pd: float) -> float:
    return score_application(credit_score, dti, ltv, pd)


if __name__ == "__main__":
    mcp.run()
