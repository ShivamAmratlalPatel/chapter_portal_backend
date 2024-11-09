"""Pagination Commands"""
from backend.inventory.inventory_models import InventoryItem


def calculate_sort_by(sort_field: str | None, sort_order: int | None) -> str | None:
    """
    Calculate sort by.

    Args:
        sort_field (str | None): Field to sort by.
        sort_order (int | None): Order to sort by.

    Returns:
        str | None: Sort by.

    """
    sort_by = None
    if sort_field is not None:
        if sort_order == 1:
            for param in InventoryItem.__table__.columns:
                if param.name == sort_field:
                    sort_by = param
        else:
            for param in InventoryItem.__table__.columns:
                if param.name == sort_field:
                    sort_by = param.desc()
    return sort_by


def calculate_filters(  # noqa: PLR0912, C901
    filters: dict[str, dict[str, str]] | None,
) -> list:
    """
    Calculate filters.

    Args:
        filters (dict[str, dict[str, str]] | None): Filters.

    Returns:
        list: Query filters.

    """
    query_filters = []

    if filters is not None:
        for key, value in filters.items():
            if value["value"] is None:
                continue
            if value["matchMode"] == "contains":
                for param in InventoryItem.__table__.columns:
                    if param.name == key:
                        query_filters.append(
                            param.ilike(f"%{value['value']}%"),
                        )
            elif value["matchMode"] == "equals":
                for param in InventoryItem.__table__.columns:
                    if param.name == key:
                        query_filters.append(
                            param == value["value"],
                        )
            elif value["matchMode"] == "startsWith":
                for param in InventoryItem.__table__.columns:
                    if param.name == key:
                        query_filters.append(
                            param.startswith(value["value"]),
                        )
            elif value["matchMode"] == "endsWith":
                for param in InventoryItem.__table__.columns:
                    if param.name == key:
                        query_filters.append(
                            param.endswith(value["value"]),
                        )
            elif value["matchMode"] == "notEquals":
                for param in InventoryItem.__table__.columns:
                    if param.name == key:
                        query_filters.append(
                            param != value["value"],
                        )
            elif value["matchMode"] == "notContains":
                for param in InventoryItem.__table__.columns:
                    if param.name == key:
                        query_filters.append(
                            ~param.ilike(f"%{value['value']}%"),
                        )

    return query_filters
