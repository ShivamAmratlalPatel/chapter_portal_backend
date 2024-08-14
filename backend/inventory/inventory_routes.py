"""Routes for inventory."""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.commands.pagination_commands import calculate_filters, calculate_sort_by
from backend.helpers import get_db
from backend.inventory.inventory_models import Category, InventoryItem, Location
from backend.inventory.inventory_schemas import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    InventoryCreate,
    InventoryRead,
    InventoryUpdate,
    LocationCreate,
    LocationRead,
    LocationUpdate,
)
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import datetime_now, generate_uuid, object_to_dict

inventory_router = APIRouter()

db_session = Depends(get_db)
current_user_instance = Depends(get_current_active_user)


@inventory_router.put("/inventory/pagination", tags=["inventory"])
def list_pagination_inventory(  # noqa: PLR0913
    filters: dict[str, dict[str, str | None]] | None = None,
    sort_field: str | None = None,
    sort_order: int | None = None,
    rows: int | None = 20,
    page: int | None = 0,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Get all inventory."""
    check_admin(current_user)
    query_filters = calculate_filters(filters)

    sort_by = calculate_sort_by(sort_field, sort_order)

    query = (
        db.query(InventoryItem)
        .filter(*query_filters)
        .filter(InventoryItem.is_deleted.is_(False))
    )

    if sort_by is not None:
        query = query.order_by(sort_by)

    query = query.offset(page * rows).limit(rows)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "customers": [
                object_to_dict(
                    InventoryRead.model_validate(inventory_item).model_dump(),
                )
                for inventory_item in query.all()
            ],
            "totalRecords": db.query(InventoryItem).filter(*query_filters).count(),
        },
    )


@inventory_router.put("/inventory/location/pagination", tags=["inventory"])
def list_pagination_inventory_location(  # noqa: PLR0913
    filters: dict[str, dict[str, str | None]] | None = None,
    sort_field: str | None = None,
    sort_order: int | None = None,
    rows: int | None = 20,
    page: int | None = 0,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Get all inventory."""
    check_admin(current_user)
    query_filters = calculate_filters(filters)

    sort_by = calculate_sort_by(sort_field, sort_order)

    query = (
        db.query(Location).filter(*query_filters).filter(Location.is_deleted.is_(False))
    )

    if sort_by is not None:
        query = query.order_by(sort_by)

    query = query.offset(page * rows).limit(rows)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "customers": [
                object_to_dict(LocationRead.model_validate(location_item).model_dump())
                for location_item in query.all()
            ],
            "totalRecords": db.query(Location).filter(*query_filters).count(),
        },
    )


@inventory_router.put("/inventory/category/pagination", tags=["inventory"])
def list_pagination_inventory_category(  # noqa: PLR0913
    filters: dict[str, dict[str, str | None]] | None = None,
    sort_field: str | None = None,
    sort_order: int | None = None,
    rows: int | None = 20,
    page: int | None = 0,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Get all inventory."""
    check_admin(current_user)
    query_filters = calculate_filters(filters)

    sort_by = calculate_sort_by(sort_field, sort_order)

    query = (
        db.query(Category).filter(*query_filters).filter(Category.is_deleted.is_(False))
    )

    if sort_by is not None:
        query = query.order_by(sort_by)

    query = query.offset(page * rows).limit(rows)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "customers": [
                object_to_dict(CategoryRead.model_validate(category_item).model_dump())
                for category_item in query.all()
            ],
            "totalRecords": db.query(Category).filter(*query_filters).count(),
        },
    )


@inventory_router.post(
    "/inventory/location",
    tags=["inventory"],
    response_model=LocationRead,
)
def create_location(
    location: LocationCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a location."""
    check_admin(current_user)
    new_location = Location(
        id=generate_uuid(),
        created_date=datetime_now(),
        name=location.name,
    )

    db.add(new_location)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(LocationRead.model_validate(new_location).model_dump()),
    )


@inventory_router.post(
    "/inventory/category",
    tags=["inventory"],
    response_model=CategoryRead,
)
def create_category(
    category: CategoryCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create a category."""
    check_admin(current_user)
    new_category = Category(
        id=generate_uuid(),
        created_date=datetime_now(),
        name=category.name,
    )

    db.add(new_category)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(CategoryRead.model_validate(new_category).model_dump()),
    )


@inventory_router.post("/inventory", tags=["inventory"], response_model=InventoryRead)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Create an inventory item."""
    check_admin(current_user)
    new_inventory = InventoryItem(
        id=generate_uuid(),
        created_date=datetime_now(),
        name=inventory.name,
        description=inventory.description,
        quantity=inventory.quantity,
        category_id=inventory.category_id,
        location_id=inventory.location_id,
    )

    db.add(new_inventory)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=object_to_dict(
            InventoryRead.model_validate(new_inventory).model_dump(),
        ),
    )


@inventory_router.put(
    "/inventory/{inventory_id}",
    tags=["inventory"],
    response_model=InventoryRead,
)
def update_inventory(
    inventory_id: str,
    inventory: InventoryUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update an inventory item."""
    check_admin(current_user)
    inventory_item: InventoryItem | None = db.get(InventoryItem, inventory_id)

    if inventory_item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Inventory item not found"},
        )

    inventory_item.name = inventory.name
    inventory_item.description = inventory.description
    inventory_item.quantity = inventory.quantity
    inventory_item.category_id = inventory.category_id
    inventory_item.location_id = inventory.location_id

    db.add(inventory_item)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(
            InventoryRead.model_validate(inventory_item).model_dump(),
        ),
    )


@inventory_router.delete(
    "/inventory/{inventory_id}",
    tags=["inventory"],
    response_model=InventoryRead,
)
def delete_inventory(
    inventory_id: str,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete an inventory item."""
    check_admin(current_user)
    inventory_item: InventoryItem | None = db.get(InventoryItem, inventory_id)

    if inventory_item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Inventory item not found"},
        )

    inventory_item.is_deleted = True

    db.add(inventory_item)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(
            InventoryRead.model_validate(inventory_item).model_dump(),
        ),
    )


@inventory_router.put(
    "/inventory/location/{location_id}",
    tags=["inventory"],
    response_model=LocationRead,
)
def update_location(
    location_id: str,
    location: LocationUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a location."""
    check_admin(current_user)
    location_item: Location | None = db.get(Location, location_id)

    if location_item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Location not found"},
        )

    location_item.name = location.name

    db.add(location_item)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(LocationRead.model_validate(location_item).model_dump()),
    )


@inventory_router.delete(
    "/inventory/location/{location_id}",
    tags=["inventory"],
    response_model=LocationRead,
)
def delete_location(
    location_id: str,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete a location."""
    check_admin(current_user)
    location_item: Location | None = db.get(Location, location_id)

    if location_item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Location not found"},
        )

    location_item.is_deleted = True

    db.add(location_item)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(LocationRead.model_validate(location_item).model_dump()),
    )


@inventory_router.put(
    "/inventory/category/{category_id}",
    tags=["inventory"],
    response_model=CategoryRead,
)
def update_category(
    category_id: str,
    category: CategoryUpdate,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Update a category."""
    check_admin(current_user)
    category_item: Category | None = db.get(Category, category_id)

    if category_item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Category not found"},
        )

    category_item.name = category.name

    db.add(category_item)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(CategoryRead.model_validate(category_item).model_dump()),
    )


@inventory_router.delete(
    "/inventory/category/{category_id}",
    tags=["inventory"],
    response_model=CategoryRead,
)
def delete_category(
    category_id: str,
    db: Session = db_session,
    current_user: UserBase = current_user_instance,
) -> JSONResponse:
    """Delete a category."""
    check_admin(current_user)
    category_item: Category | None = db.get(Category, category_id)

    if category_item is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Category not found"},
        )

    category_item.is_deleted = True

    db.add(category_item)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=object_to_dict(CategoryRead.model_validate(category_item).model_dump()),
    )
