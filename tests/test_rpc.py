import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_rpc_no_payload():
    # Empty JSON-RPC payload should return a JSON-RPC error object
    response = client.post("/rpc", json={})
    assert response.status_code == 200
    body = response.json()
    assert body.get("jsonrpc") == "2.0"
    assert "error" in body
