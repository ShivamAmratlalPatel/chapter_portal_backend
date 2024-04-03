"""Test the behavior of your application after merging Alembic scripts."""
import pytest
from fastapi.testclient import TestClient
from starlette import status

from alembic import command
from alembic.config import Config
from backend.main import app
from testing.fixtures.database import session, session_factory  # noqa: F401


@pytest.fixture(scope="session")
def alembic_config() -> Config:
    """Get the Alembic configuration."""
    return Config("alembic.ini")


@pytest.fixture(scope="session")
def _alembic_upgrade(alembic_config: Config) -> None:
    """Upgrade to head revision."""
    command.upgrade(alembic_config, "head")


@pytest.fixture(scope="session")
def _alembic_downgrade(alembic_config: Config) -> None:
    """Downgrade to base revision."""
    command.downgrade(alembic_config, "base")


@pytest.fixture(scope="session")
def client(_alembic_upgrade: None) -> TestClient:
    """Get a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.mark.usefixtures("_alembic_downgrade")
def test_alembic_merge_scripts(client: TestClient) -> None:
    """Test the behaviour of your application after merging Alembic scripts."""
    response = client.get("/health")

    assert response.status_code == status.HTTP_200_OK
