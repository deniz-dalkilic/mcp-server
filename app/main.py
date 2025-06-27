from fastapi import FastAPI

app = FastAPI(title="MCP Local Server")

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
