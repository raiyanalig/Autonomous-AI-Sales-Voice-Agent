"""Shared pytest fixtures.

Adds the backend directory to sys.path so `app` is importable, and exposes
a TestClient that triggers FastAPI lifespan events.
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure the backend/ directory is on sys.path (backend/tests/../)
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.main import app  # noqa: E402


@pytest.fixture
def client():
    """TestClient with lifespan events triggered."""
    with TestClient(app) as test_client:
        yield test_client
