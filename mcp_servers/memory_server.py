from mcp.server.fastmcp import FastMCP

from tools.memory_tools import memory_save, memory_search

mcp = FastMCP("credit-memory")


@mcp.tool()
def memory_search_tool(session_id: str, query: str = "", limit: int = 5):
    """Search PostgreSQL + Chroma memory for a session."""
    return memory_search(session_id, query=query, limit=limit)


@mcp.tool()
def memory_save_tool(session_id: str, content: str, kind: str = "note") -> dict:
    """Persist an interaction into PostgreSQL and Chroma."""
    return memory_save(session_id, content, kind=kind)


if __name__ == "__main__":
    from mcp_servers.serve import run_mcp

    run_mcp(mcp, 8103)
