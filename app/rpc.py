from fastapi import APIRouter
from mcp.server.fastmcp import FastMCP
from app.tools import load_tools

# 1) Create your MCP server
mcp = FastMCP(name="My MCP Server", stateless_http=True)

# 2) Register all your tools
for tool_def in load_tools():
    mcp.register_tool(tool_def)

# 3) Expose it via FastAPI
router = APIRouter()
router.mount("/rpc", mcp.streamable_http_app())
