"""Allocation Schemas"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.utils import generate_uuid


class AllocationBase(BaseModel):
    """Allocation Base"""

    section_id: int
    chapter_id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "section_id": 1,
            "chapter_id": generate_uuid(),
        },
    )


class AllocationCreate(AllocationBase):
    """Allocation Create"""

    user_name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **AllocationBase.model_config["json_schema_extra"],
            "user_name": "User Name",
        },
    )


class AllocationRead(AllocationBase):
    """Allocation Read"""

    id: UUID
    user_name: str
    section_name: str
    chapter_name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            **AllocationBase.model_config["json_schema_extra"],
            "id": generate_uuid(),
            "user_name": "User Name",
            "section_name": "Section Name",
            "chapter_name": "Chapter Name",
        },
    )
