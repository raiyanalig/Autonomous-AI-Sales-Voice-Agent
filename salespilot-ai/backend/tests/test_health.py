"""Tests for health, readiness, validation, errors, middleware and CORS."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.exceptions import register_exception_handlers

HEALTH_URL = "/api/v1/health"
READY_URL = "/api/v1/health/ready"


# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

def test_health_returns_200(client):
    response = client.get(HEALTH_URL)
    assert response.status_code == 200


def test_health_contains_correct_application_name(client):
    response = client.get(HEALTH_URL)
    body = response.json()
    assert body["status"] == "healthy"
    assert body["application"] == "SalesPilot AI"


# ---------------------------------------------------------------------------
# Readiness endpoint
# ---------------------------------------------------------------------------

def test_readiness_endpoint_works(client):
    response = client.get(READY_URL)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["application"] == "SalesPilot AI"
    assert isinstance(body["checks"], list)


# ---------------------------------------------------------------------------
# Request validation
# ---------------------------------------------------------------------------

def test_invalid_input_returns_validation_error(client):
    payload = {"name": "", "email": "not-an-email", "age": 12}
    response = client.post("/api/v1/demo/validate", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["status"] == "error"
    assert "detail" in body


def test_valid_input_passes_validation(client):
    payload = {"name": "Rahul", "email": "rahul@example.com", "age": 22}
    response = client.post("/api/v1/demo/validate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Validation passed for Rahul"
    assert body["received"]["email"] == "rahul@example.com"


# ---------------------------------------------------------------------------
# Unknown routes
# ---------------------------------------------------------------------------

def test_unknown_route_returns_404(client):
    response = client.get("/api/v1/nonexistent")
    assert response.status_code == 404
    assert response.json()["status"] == "error"


# ---------------------------------------------------------------------------
# Unexpected errors
# ---------------------------------------------------------------------------

def test_unexpected_errors_handled():
    """A raising endpoint must be converted to a 500 JSON error, no traceback leaked."""
    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.get("/boom")
    async def boom():
        raise RuntimeError("boom")

    test_client = TestClient(test_app, raise_server_exceptions=False)
    response = test_client.get("/boom")
    assert response.status_code == 500
    body = response.json()
    assert body["status"] == "error"
    assert "boom" not in body["message"]


# ---------------------------------------------------------------------------
# Request ID middleware
# ---------------------------------------------------------------------------

def test_request_id_returned_in_response_header(client):
    response = client.get(HEALTH_URL)
    assert "x-request-id" in response.headers
    assert response.headers["x-request-id"]


def test_request_id_reuses_incoming_header(client):
    response = client.get(HEALTH_URL, headers={"X-Request-ID": "test-request-123"})
    assert response.headers["x-request-id"] == "test-request-123"


# ---------------------------------------------------------------------------
# CORS middleware
# ---------------------------------------------------------------------------

def test_cors_allows_configured_origin(client):
    response = client.get(HEALTH_URL, headers={"Origin": "http://localhost:5173"})
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_cors_rejects_unknown_origin(client):
    response = client.get(HEALTH_URL, headers={"Origin": "http://evil.example.com"})
    assert "access-control-allow-origin" not in response.headers
