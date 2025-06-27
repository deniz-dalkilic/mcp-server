from fastapi import FastAPI, Request, HTTPException

app = FastAPI(title="MCP Local Server")

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

@app.post("/rpc")
async def dummy_rpc(request: Request):
    # For now, any POST /rpc returns 500 as per our tests
    raise HTTPException(status_code=500)
