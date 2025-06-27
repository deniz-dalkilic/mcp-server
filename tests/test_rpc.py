import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    # health check
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_rpc_no_payload(monkeypatch):
    # sample error test
    response = client.post("/rpc", json={})
    assert response.status_code == 500
