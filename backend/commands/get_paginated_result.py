"""Get paginated result command."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from sqlakeyset import get_page
from sqlalchemy import Column, nulls_first, nulls_last
from sqlalchemy.orm import Query

from backend.schemas import NextPage, PaginationResult, SortBy
from backend.utils import object_to_dict


class GetPaginatedResult:
    """Get paginated result command."""

    def __init__(self: "GetPaginatedResult") -> None:
        """Initialize GetPaginatedResult command."""

    def run(  # noqa: PLR0913
        self: "GetPaginatedResult",
        cursor_id: UUID | None,
        cursor_column: datetime | str | None,
        previous: bool | None,
        query: Query,
        schema: type[BaseModel],
        per_page: int = 20,
    ) -> PaginationResult:
        """
        Get paginated result.

        Args:
            cursor_id (UUID | None): Cursor id.
            cursor_column (datetime | str | None): Cursor column.
            previous (bool | None): Previous.
            query (Query): Query.
            schema (type[BaseModel]): Schema.
            per_page (int, optional): Per page. Defaults to 20.

        Returns:
            PaginationResult: Pagination result.

        """
        if cursor_column and cursor_id:
            page = ((cursor_column, cursor_id), previous)
        else:
            page = None

        query_result = get_page(query, per_page=per_page, page=page)
        next_query = query_result.paging.next
        previous = query_result.paging.previous
        return PaginationResult(
            next=NextPage(
                previous=False,
                cursor_column=next_query[0][0],
                cursor_id=next_query[0][1],
            )
            if query_result.paging.has_next
            else None,
            previous=NextPage(
                previous=True,
                cursor_column=previous[0][0],
                cursor_id=previous[0][1],
            )
            if query_result.paging.has_previous
            else None,
            results=[
                object_to_dict(schema.model_validate(ta), format_date=True)
                for ta in query_result
            ],
        )

    def get_sort_by(  # noqa: PLR0911
        self: "GetPaginatedResult",
        date_column: Column,
        name_column: Column,
        sort_by: SortBy,
        move_in_column: Column | None = None,
    ) -> Column | None:
        """
        Get sort by.

        Args:
            date_column (Column): Date column.
            name_column (Column): Name column.
            sort_by (SortBy): Sort by.
            move_in_column (Column, optional): Move in column. Defaults to None.

        Returns:
            Column | None: Column.

        """
        if sort_by == SortBy.date_asc:
            return date_column.asc()
        elif sort_by == SortBy.date_desc:
            return date_column.desc()
        elif sort_by == SortBy.a_z_asc:
            return name_column.asc()
        elif sort_by == SortBy.a_z_desc:
            return name_column.desc()
        elif sort_by == SortBy.move_in_asc:
            return nulls_first(move_in_column.asc())
        elif sort_by == SortBy.move_in_desc:
            return nulls_last(move_in_column.desc())
        return None
