"""Tests for the health endpoint."""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    """GET /api/v1/health returns the expected payload."""
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "application": "SalesPilot AI"}


def test_root_endpoint() -> None:
    """GET / returns API navigation links."""
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["application"] == "SalesPilot AI"
    assert body["docs"] == "/docs"
    assert body["health"] == "/api/v1/health"
