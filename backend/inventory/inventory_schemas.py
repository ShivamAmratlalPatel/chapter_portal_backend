"""Inventory schemas"""
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from backend.utils import generate_uuid


class CategoryCreate(BaseModel):
    """Category create."""

    name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Category",
            },
        },
    )


class CategoryUpdate(CategoryCreate):
    """Category update."""

    pass


class CategoryRead(CategoryCreate):
    """Category read."""

    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": generate_uuid(),
                **CategoryCreate.model_config["json_schema_extra"]["example"],
            },
        },
    )


class LocationCreate(BaseModel):
    """Location create."""

    name: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Location",
            },
        },
    )


class LocationUpdate(LocationCreate):
    """Location update."""

    pass


class LocationRead(LocationCreate):
    """Location read."""

    id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": generate_uuid(),
                **LocationCreate.model_config["json_schema_extra"]["example"],
            },
        },
    )


class InventoryCreate(BaseModel):
    """Inventory create."""

    name: str
    description: str | None = None
    quantity: int | None = None
    category_id: UUID | None = None
    location_id: UUID | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Item",
                "description": "Item description",
                "quantity": 1,
                "category_id": generate_uuid(),
                "location_id": generate_uuid(),
            },
        },
    )


class InventoryRead(InventoryCreate):
    """Inventory read."""

    id: UUID
    category: CategoryRead | None = None
    location: LocationRead | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": generate_uuid(),
                **InventoryCreate.model_config["json_schema_extra"]["example"],
                "category": CategoryRead.model_config["json_schema_extra"]["example"],
                "location": LocationRead.model_config["json_schema_extra"]["example"],
            },
        },
    )


class InventoryUpdate(InventoryCreate):
    """Inventory update."""

    pass
