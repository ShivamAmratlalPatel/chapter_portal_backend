"""Test the main module."""
from fastapi.testclient import TestClient
from starlette import status

from testing.fixtures.client import client  # noqa: F401
from testing.fixtures.database import session, session_factory  # noqa: F401


def test_health(client: TestClient) -> None:
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "ok"


def test_trace(client: TestClient) -> None:
    """Test the trace endpoint."""
    response = client.get("/tracemalloc")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "First snapshot taken!\n"
