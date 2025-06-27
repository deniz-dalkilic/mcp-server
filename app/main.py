from fastapi import FastAPI, Request, HTTPException
from mcp.server.fastmcp import FastMCP
from app.tools import load_tools

app = FastAPI(title="MCP Local Server")

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

@app.post("/rpc")
async def rpc_fallback(request: Request):
    # test için POST /rpc isteklerine 500 dön
    raise HTTPException(status_code=500)

# Initialize FastMCP for JSON-RPC over HTTP
mcp = FastMCP(name="MCP Local Server", stateless_http=True)

# Register tools dynamically by binding the tool's __call__ method
for method, tool in load_tools().items():
    mcp.tool(name=method, description=tool.__doc__)(tool.__call__)

# Mount the MCP ASGI app at /rpc/ (for subpaths)
app.mount("/rpc/", mcp.streamable_http_app())
