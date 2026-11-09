from mcp.server.fastmcp import FastMCP

from tools.credit_tools import credit_risk_prediction
from tools.database_tools import sql_database_query
from tools.financial_tools import financial_calculator
from tools.python_tools import run_python

mcp = FastMCP("credit-analyst")


@mcp.tool()
def financial_calculator_tool(
    monthly_income: float,
    existing_emi: float,
    loan_amount: float,
    tenure_months: int,
    annual_rate: float = 0.13,
) -> dict:
    """Compute EMI, FOIR, DTI and surplus from applicant numbers."""
    return financial_calculator(
        monthly_income, existing_emi, loan_amount, tenure_months, annual_rate
    )


@mcp.tool()
def sql_database_query_tool(sql: str) -> list[dict]:
    """Run a read-only SELECT against the product/borrower database."""
    return sql_database_query(sql)


@mcp.tool()
def python_code_execution(expression: str) -> str:
    """Evaluate a sandboxed EMI/FOIR expression."""
    return run_python(expression)


@mcp.tool()
def credit_risk_prediction_tool(
    credit_score: float,
    monthly_income: float,
    existing_emi: float,
    loan_amount: float,
    tenure_months: int,
    annual_rate: float = 0.13,
    defaults: float = 0,
) -> dict:
    """Estimate illustrative PD and application score with the sklearn model."""
    return credit_risk_prediction(
        credit_score,
        monthly_income,
        existing_emi,
        loan_amount,
        tenure_months,
        annual_rate,
        defaults,
    )


if __name__ == "__main__":
    from mcp_servers.serve import run_mcp

    run_mcp(mcp, 8102)
