import pytest
from fastapi.testclient import TestClient
from simulation_server import app
import os

client = TestClient(app)

def test_cors_options_allowed():
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:8080",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:8080"

def test_cors_options_disallowed():
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://evil.com",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert response.status_code == 400
