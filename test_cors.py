from fastapi.testclient import TestClient
import os

# Set env var for testing BEFORE importing the app
os.environ["ALLOWED_ORIGINS"] = "http://localhost:8080,https://example.com"

from simulation_server import app

client = TestClient(app)

def test_cors_allowed_origin():
    headers = {
        "Origin": "http://localhost:8080",
        "Access-Control-Request-Method": "GET"
    }
    response = client.options("/api/health", headers=headers)
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:8080"

def test_cors_disallowed_origin():
    headers = {
        "Origin": "http://malicious.com",
        "Access-Control-Request-Method": "GET"
    }
    response = client.options("/api/health", headers=headers)
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
