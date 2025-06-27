from fastapi import FastAPI
from app.rpc import router as rpc_router

app = FastAPI(title="MCP Local Server")

# Health check
@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

# JSON-RPC endpoint
app.include_router(rpc_router, prefix="/rpc", tags=["rpc"])
