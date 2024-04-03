"""Test client fixture for FastAPI app."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend.helpers import get_db
from backend.main import app


@pytest.fixture()
def client(session: Session) -> TestClient:
    """Generate test client."""
    app.dependency_overrides[get_db] = lambda: session

    yield TestClient(app)

    app.dependency_overrides = {}
