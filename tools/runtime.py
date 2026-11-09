"""Local catalog of MCP tool implementations.

MCP servers wrap these functions. Agents call `invoke()` so tests and CLI
work without spawning MCP processes. Set USE_MCP=true to route through MCP HTTP.
"""

from __future__ import annotations

from typing import Any, Callable

from core.config import get_settings
from tools.credit_tools import credit_risk_prediction
from tools.database_tools import search_loan_products, sql_database_query
from tools.financial_tools import financial_calculator
from tools.memory_tools import memory_save, memory_search
from tools.python_tools import run_python
from tools.research_tools import credit_policy_retriever, document_retriever, web_search

TOOL_IMPLS: dict[str, Callable[..., Any]] = {
    "web_search": web_search,
    "loan_product_search": search_loan_products,
    "document_retriever": document_retriever,
    "credit_policy_retriever": credit_policy_retriever,
    "financial_calculator": financial_calculator,
    "sql_database_query": sql_database_query,
    "python_code_execution": run_python,
    "credit_risk_prediction": credit_risk_prediction,
    "memory_search": memory_search,
    "memory_save": memory_save,
}


def invoke(name: str, **kwargs: Any) -> Any:
    if name not in TOOL_IMPLS:
        raise KeyError(f"Unknown tool: {name}")
    if get_settings().use_mcp:
        try:
            return _invoke_via_mcp(name, kwargs)
        except Exception:
            return TOOL_IMPLS[name](**kwargs)
    return TOOL_IMPLS[name](**kwargs)


def mcp_connections() -> dict:
    settings = get_settings()
    return {
        "research": {"url": settings.mcp_research_url, "transport": "http"},
        "analyst": {"url": settings.mcp_analyst_url, "transport": "http"},
        "memory": {"url": settings.mcp_memory_url, "transport": "http"},
    }


def _invoke_via_mcp(name: str, kwargs: dict) -> Any:
    import asyncio

    from langchain_mcp_adapters.client import MultiServerMCPClient

    async def _run():
        client = MultiServerMCPClient(mcp_connections())
        tools = await client.get_tools()
        tool = next(t for t in tools if t.name == name)
        return await tool.ainvoke(kwargs)

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(_run())
    return TOOL_IMPLS[name](**kwargs)
