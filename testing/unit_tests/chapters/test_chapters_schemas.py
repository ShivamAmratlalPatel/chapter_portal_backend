"""Test Chapter schemas."""
from datetime import datetime
from uuid import UUID

import pytest
import pytz
from pydantic import ValidationError

from backend.chapters.chapters_schemas import (
    ChapterBase,
    ChapterCreate,
    ChapterRead,
    ChapterUpdate,
    ZoneEnum,
)


def test_valid_chapter_base_schema() -> None:
    """Test valid ChapterBase schema."""
    data = {
        "name": "Imperial",
        "email": "hindu_society@imperial.ac.uk",
        "zone": ZoneEnum.london,
    }
    chapter_base = ChapterBase(**data)
    assert chapter_base.name == data["name"]
    assert chapter_base.email == data["email"]
    assert chapter_base.zone == ZoneEnum.london


def test_invalid_chapter_base_schema() -> None:
    """Test invalid ChapterBase schema."""
    invalid_data = {
        "name": "Imperial",
        "email": "invalid_email",
        "zone": "UnknownZone",
    }
    with pytest.raises(ValidationError):
        ChapterBase(**invalid_data)


def test_valid_chapter_create_schema() -> None:
    """Test valid ChapterCreate schema."""
    data = {
        "name": "Imperial",
        "email": "hindu_society@imperial.ac.uk",
        "zone": ZoneEnum.london,
    }
    chapter_create = ChapterCreate(**data)
    assert chapter_create.name == data["name"]
    assert chapter_create.email == data["email"]
    assert chapter_create.zone == ZoneEnum.london


def test_valid_chapter_update_schema() -> None:
    """Test valid ChapterUpdate schema."""
    data = {
        "name": "Imperial",
        "email": "hindu_society@imperial.ac.uk",
        "zone": ZoneEnum.london,
    }
    chapter_update = ChapterUpdate(**data)
    assert chapter_update.name == data["name"]
    assert chapter_update.email == data["email"]
    assert chapter_update.zone == ZoneEnum.london


def test_valid_chapter_read_schema() -> None:
    """Test valid ChapterRead schema."""
    data = {
        "id": "d9b9c6c0-6e2d-4e9f-9b1a-1d3d0a7e0f4e",
        "name": "Imperial",
        "email": "hindu_society@imperial.ac.uk",
        "zone": ZoneEnum.london,
        "created_date": datetime(2021, 1, 1, tzinfo=pytz.timezone("Europe/London")),
        "last_modified_date": datetime(
            2021,
            1,
            1,
            tzinfo=pytz.timezone("Europe/London"),
        ),
        "is_deleted": False,
    }
    chapter_read = ChapterRead(**data)
    assert chapter_read.id == UUID(data["id"])
    assert chapter_read.name == data["name"]
    assert chapter_read.email == data["email"]
    assert chapter_read.zone == ZoneEnum.london
    assert chapter_read.created_date == data["created_date"]
    assert chapter_read.last_modified_date == data["last_modified_date"]
    assert chapter_read.is_deleted == data["is_deleted"]
