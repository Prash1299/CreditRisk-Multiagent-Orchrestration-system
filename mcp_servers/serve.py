import os

from mcp.server.fastmcp import FastMCP


def run_mcp(server: FastMCP, default_port: int) -> None:
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport in {"http", "streamable-http", "sse"}:
        port = int(os.getenv("PORT", default_port))
        host = os.getenv("MCP_HOST", "0.0.0.0")
        server.run(transport="streamable-http", host=host, port=port)
    else:
        server.run()
