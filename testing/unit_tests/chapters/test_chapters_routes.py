"""
Module: test_chapter_routes

This module contains unit tests for the FastAPI routes related to chapter creation and handling.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from backend.helpers import get_db
from backend.main import app
from backend.utils import generate_uuid
from testing.fixtures.database import session, session_factory  # noqa: F401
from testing.helpers.fake_data import fake_chapter, fake_email, fake_name


@pytest.fixture()
def client(
    session: Session,
) -> TestClient:
    """
    Fixture Function: client

    Generate a test client with the provided database session.

    Args:
       session (Session): A SQLAlchemy database session.

    Yields:
       TestClient: A FastAPI test client configured to use the provided session.
    """
    app.dependency_overrides[get_db] = lambda: session

    yield TestClient(app)

    app.dependency_overrides = {}


class TestPostChapter:
    """
    Test Class: TestPostChapter

    This class contains unit tests for the POST /chapter route.
    """

    def test_post_chapter(self: "TestPostChapter", client: TestClient) -> None:
        """
        Test Method: test_post_chapter

        Test the POST /chapter route for successful chapter creation.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_chapter()

        response = client.post("/chapter", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["email"] == data["email"]
        assert response.json()["zone"] == data["zone"]

    def test_post_chapter_invalid_email(
        self: "TestPostChapter",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_post_chapter_invalid_email

        Test the POST /chapter route with invalid email format.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_chapter()
        data["email"] = "invalid_email"

        response = client.post("/chapter", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["msg"] == (
            "value is not a valid email address: The email address is not valid. It must "
            "have exactly one @-sign."
        )
        assert response.json()["detail"][0]["type"] == "value_error"
        assert response.json()["detail"][0]["loc"] == ["body", "email"]

    def test_post_chapter_invalid_zone(
        self: "TestPostChapter",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_post_chapter_invalid_zone

        Test the POST /chapter route with an invalid zone value.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_chapter()
        data["zone"] = "invalid_zone"

        response = client.post("/chapter", json=data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json()["detail"][0]["msg"] == (
            "Input should be 'London','South','North' or 'Central'"
        )
        assert response.json()["detail"][0]["type"] == "enum"
        assert response.json()["detail"][0]["loc"] == ["body", "zone"]

    def test_duplicate_chapter(self: "TestPostChapter", client: TestClient) -> None:
        """
        Test Method: test_duplicate_chapter

        Test the scenario where a chapter with the same data already exists.

        Args:
            client (TestClient): A FastAPI test client.



        Returns:
           None
        """
        data = fake_chapter()

        response = client.post("/chapter", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["email"] == data["email"]
        assert response.json()["zone"] == data["zone"]

        response = client.post("/chapter", json=data)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "Chapter already exists"


class TestGetChapter:
    """
    Test Class: TestGetChapter

    This class contains unit tests for the GET /chapter/{chapter_id} route.
    """

    def test_get_chapter(
        self: "TestGetChapter",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_chapter

        Test the GET /chapter/{chapter_id} route for successful chapter retrieval.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_chapter()

        response = client.post("/chapter", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["email"] == data["email"]
        assert response.json()["zone"] == data["zone"]

        response = client.get(f"/chapter/{response.json()['id']}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == data["name"]
        assert response.json()["email"] == data["email"]
        assert response.json()["zone"] == data["zone"]

    def test_get_chapter_not_found(
        self: "TestGetChapter",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_chapter_not_found

        Test the GET /chapter/{chapter_id} route for a chapter that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get(f"/chapter/{generate_uuid()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Chapter not found"


class TestGetChapterList:
    """
    Test Class: TestGetChapterList

    This class contains unit tests for the GET /chapters route.
    """

    def test_get_chapter_list(
        self: "TestGetChapterList",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_chapter_list

        Test the GET /chapters route for successful chapter retrieval.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_chapter()

        response = client.post("/chapter", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["email"] == data["email"]
        assert response.json()["zone"] == data["zone"]

        response = client.get("/chapters")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == data["name"]
        assert response.json()[0]["email"] == data["email"]
        assert response.json()[0]["zone"] == data["zone"]

    def test_get_chapter_list_empty(
        self: "TestGetChapterList",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_get_chapter_list_empty

        Test the GET /chapters route for a chapter that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.get("/chapters")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Chapters not found"


class TestPutChapter:
    """
    Test Class: TestPutChapter

    This class contains unit tests for the PUT /chapter/{chapter_id} route.
    """

    def test_put_chapter(
        self: "TestPutChapter",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_put_chapter

        Test the PUT /chapter/{chapter_id} route for successful chapter update.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_chapter()

        response = client.post("/chapter", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["email"] == data["email"]
        assert response.json()["zone"] == data["zone"]

        data["name"] = fake_name()
        data["email"] = fake_email()
        data["zone"] = "South"

        response = client.put(f"/chapter/{response.json()['id']}", json=data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["name"] == data["name"]
        assert response.json()["email"] == data["email"]
        assert response.json()["zone"] == data["zone"]

    def test_put_chapter_not_found(
        self: "TestPutChapter",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_put_chapter_not_found

        Test the PUT /chapter/{chapter_id} route for a chapter that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_chapter()

        response = client.put(f"/chapter/{generate_uuid()}", json=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Chapter not found"


class TestDeleteChapter:
    """
    Test Class: TestDeleteChapter

    This class contains unit tests for the DELETE /chapter/{chapter_id} route.
    """

    def test_delete_chapter(
        self: "TestDeleteChapter",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_delete_chapter

        Test the DELETE /chapter/{chapter_id} route for successful chapter deletion.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        data = fake_chapter()

        response = client.post("/chapter", json=data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["name"] == data["name"]
        assert response.json()["email"] == data["email"]
        assert response.json()["zone"] == data["zone"]

        response = client.delete(f"/chapter/{response.json()['id']}")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.json() == {}

    def test_delete_chapter_not_found(
        self: "TestDeleteChapter",
        client: TestClient,
    ) -> None:
        """
        Test Method: test_delete_chapter_not_found

        Test the DELETE /chapter/{chapter_id} route for a chapter that does not exist.

        Args:
           client (TestClient): A FastAPI test client.

        Returns:
           None
        """
        response = client.delete(f"/chapter/{generate_uuid()}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Chapter not found"
