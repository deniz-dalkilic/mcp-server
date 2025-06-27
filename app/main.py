from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.tools import load_tools


app = FastAPI(title="MCP Local Server")

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

@app.post("/rpc")
async def rpc_endpoint(request: Request):
    payload = await request.json()
    # JSON-RPC 2.0: validate 'method'
    method = payload.get("method")
    if not method:
        # Invalid Request
        return JSONResponse(status_code=200, content={
            "jsonrpc": "2.0",
            "error": {"code": -32600, "message": "Invalid Request"},
            "id": payload.get("id")
        })
    tools = load_tools()
    if method not in tools:
        # Method not found
        return JSONResponse(status_code=200, content={
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": "Method not found"},
            "id": payload.get("id")
        })
    # Call the tool
    tool = tools[method]
    params = payload.get("params", {}) or {}
    try:
        result = await tool(**params)
        return {"jsonrpc": "2.0", "result": result, "id": payload.get("id")}
    except Exception as exc:
        # Internal error
        return JSONResponse(status_code=200, content={
            "jsonrpc": "2.0",
            "error": {"code": -32603, "message": str(exc)},
            "id": payload.get("id")
        })
