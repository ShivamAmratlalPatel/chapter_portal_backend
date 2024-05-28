"""Inventory schemas"""
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.utils import generate_uuid


class CategoryRead(BaseModel):
    """Category read."""

    id: UUID
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": generate_uuid(),
                "name": "Category",
            },
        },
    )


class LocationRead(BaseModel):
    """Location read."""

    id: UUID
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": generate_uuid(),
                "name": "Location",
            },
        },
    )


class InventoryRead(BaseModel):
    """Inventory read."""

    id: UUID
    name: str
    description: str | None = None
    quantity: int | None = None
    category_id: UUID | None = None
    location_id: UUID | None = None
    category: CategoryRead | None = None
    location: LocationRead | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": generate_uuid(),
                "name": "Item",
                "description": "Item description",
                "quantity": 1,
                "category_id": generate_uuid(),
                "location_id": generate_uuid(),
                "category": CategoryRead.model_config["json_schema_extra"]["example"],
                "location": LocationRead.model_config["json_schema_extra"]["example"],
            },
        },
    )
