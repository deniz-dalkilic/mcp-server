from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from app.tools import load_tools

app = FastAPI(title="MCP Local Server")

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

@app.post("/rpc")
async def rpc_endpoint(request: Request):
    # Simple JSON-RPC error response for invalid requests
    payload = await request.json()
    return JSONResponse(
        status_code=200,
        content={
            "jsonrpc": "2.0",
            "error": {"code": -32600, "message": "Invalid Request"},
            "id": payload.get("id"),
        },
    )

# Initialize FastMCP for JSON-RPC over HTTP for JSON-RPC over HTTP
mcp = FastMCP(name="MCP Local Server", stateless_http=True)

# Register tools dynamically by binding the tool's __call__ method
for method, tool in load_tools().items():
    mcp.tool(name=method, description=tool.__doc__)(tool.__call__)

# Mount the MCP ASGI app at /rpc and /rpc/
app.mount("/rpc", mcp.streamable_http_app())
app.mount("/rpc/", mcp.streamable_http_app())
