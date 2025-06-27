from fastapi import APIRouter, Request, HTTPException
from modelcontextprotocol_python import RPCDispatcher

from app.tools import load_tools

router = APIRouter()
dispatcher = RPCDispatcher(tools=load_tools())

@router.post("/")
async def handle_rpc(request: Request):
    payload = await request.json()
    try:
        return await dispatcher.dispatch(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
