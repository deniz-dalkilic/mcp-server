import pytest
import httpx
from app.tools.scholar_tool import ScholarTool

# Sample CrossRef response payload
CROSSREF_SAMPLE = {
    "message": {
        "items": [
            {
                "title": ["Sample Article Title"],
                "container-title": ["Journal of Testing"],
                "author": [{"given": "John", "family": "Doe"}],
                "issued": {"date-parts": [[2023, 5, 1]]},
                "DOI": "10.1234/example.doi",
                "URL": "https://doi.org/10.1234/example.doi"
            }
        ]
    }
}

@pytest.mark.asyncio
async def test_search_articles_parsing(monkeypatch):
    # Stub HTTP client transport
    transport = httpx.MockTransport(lambda req: httpx.Response(200, json=CROSSREF_SAMPLE))
    tool = ScholarTool(max_results=1, polite_delay_ms=0)
    # Replace internal client
    tool._client = httpx.AsyncClient(transport=transport)

    # Call with filters
    result = await tool.search_articles(
        query="test", max_results=1, since_year=2023, until_year=2023
    )

    assert isinstance(result, list)
    assert len(result) == 1
    article = result[0]
    assert article["title"] == "Sample Article Title"
    assert article["journal"] == "Journal of Testing"
    assert article["authors"] == ["Doe, John"]
    assert article["year"] == 2023
    assert article["doi"] == "10.1234/example.doi"
    assert article["url"] == "https://doi.org/10.1234/example.doi"


# tests/test_rpc_call.py
from fastapi.testclient import TestClient
import pytest
import httpx
import json

from app.main import app

client = TestClient(app)

# Monkeypatch load_tools to return a dummy tool
class DummyTool:
    __doc__ = "Dummy tool for testing"
    async def __call__(self, **params):
        return {"echo": params}

@pytest.fixture(autouse=True)
def patch_tools(monkeypatch):
    monkeypatch.setattr('app.main.load_tools', lambda: {"scholar.search_articles": DummyTool()})

def test_rpc_echo_tool():
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "scholar.search_articles",
        "params": {"foo": "bar"}
    }
    response = client.post(
        "/rpc", data=json.dumps(payload), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["jsonrpc"] == "2.0"
    assert data["id"] == 1
    assert data["result"]["echo"]["foo"] == "bar"

# tests/test_rpc_errors.py
from fastapi.testclient import TestClient
from app.main import app
import pytest
import json

client = TestClient(app)

def test_rpc_invalid_request():
    # Missing 'method'
    payload = {"jsonrpc": "2.0", "id": 1}
    response = client.post(
        "/rpc", data=json.dumps(payload), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"]["code"] == -32600


def test_rpc_method_not_found():
    payload = {"jsonrpc": "2.0", "id": 2, "method": "unknown.method"}
    response = client.post(
        "/rpc", data=json.dumps(payload), headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["error"]["code"] == -32601
