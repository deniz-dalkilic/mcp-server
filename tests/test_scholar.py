import pytest
import httpx
from app.tools.scholar_tool import ScholarTool

@pytest.mark.asyncio
async def test_scholar_stub(monkeypatch):

    fake = {"message": {"items": []}}
    transport = httpx.MockTransport(lambda req: httpx.Response(200, json=fake))
    tool = ScholarTool()
    tool._client = httpx.AsyncClient(transport=transport)
    out = await tool("any query")
    assert isinstance(out, list)
    assert out == []
