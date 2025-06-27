from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_rpc_no_payload():
    # Empty JSON-RPC payload should return a JSON-RPC error object per spec
    response = client.post("/rpc", json={})
    assert response.status_code == 200
    body = response.json()
    # Must be JSON-RPC 2.0 response
    assert body.get("jsonrpc") == "2.0"
    # Check Invalid Request error code and message
    assert body.get("error", {}).get("code") == -32600
    assert body.get("error", {}).get("message") == "Invalid Request"
    # 'id' must be null for invalid requests
    assert body.get("id") is None
