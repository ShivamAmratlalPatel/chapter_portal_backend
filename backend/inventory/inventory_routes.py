"""Routes for inventory."""

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from backend.commands.pagination_commands import calculate_filters, calculate_sort_by
from backend.helpers import get_db
from backend.inventory.inventory_models import InventoryItem
from backend.inventory.inventory_schemas import InventoryRead
from backend.users.users_commands.check_admin import check_admin
from backend.users.users_commands.get_users import get_current_active_user
from backend.users.users_schemas import UserBase
from backend.utils import object_to_dict

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

    query = db.query(InventoryItem).filter(*query_filters)

    if sort_by is not None:
        query = query.order_by(sort_by)

    query = query.offset(page * rows).limit(rows)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "customers": [
                object_to_dict(
                    InventoryRead.model_validate(inventory_item).model_dump()
                )
                for inventory_item in query.all()
            ],
            "totalRecords": db.query(InventoryItem).filter(*query_filters).count(),
        },
    )
