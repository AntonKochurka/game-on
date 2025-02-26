from fastapi import Request
from typing import Type, Any, List, Optional, Dict
from sqlalchemy import select, func, asc, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from pydantic import BaseModel, Field
from typing_extensions import Literal

from app.core.settings import settings

class DefaultPaginatorQueries(BaseModel):
    page: int = Field(1, gt=0, description="Page number (1-based)")
    per_page: int | None = Field(None, gt=0, description="Items per page")
    sort_by: str = Field("created_at", description="Field to sort by")
    order: str = Field("asc", description="Sorting direction: asc|desc")

class PaginatorResult(BaseModel):
    items: List[Dict[str, Any]]
    page: int
    total_pages: int
    total_items: int


class PaginatorService:
    """
    Generic async pagination service for SQLAlchemy models.
    
    Supported filter operators in apply_filters:
    - eq (default): Equal
    - ne: Not equal
    - gt: Greater than
    - lt: Less than
    - in: In list
    - like: Like pattern
    """

    def __init__(
        self, session: AsyncSession, 
        model: Type[Any], item_model: BaseModel
    ) -> None:
        self.session = session
        self.model = model
        self.item_model = item_model
        self._query = select(self.model)

    def apply_filters(self, request: Request | None = None, **filters: Any) -> "PaginatorService":
        """
        Apply filter conditions to the query.
        Use field__operator syntax: age__gt=25, name__like='John%'
        """
        if request is not None:
            filters.update({
                key: value for key, value in request.query_params.items()
                if key not in {"page", "per_page", "sort_by", "order"} 
                and key in set(self.item_model.model_fields.keys()) 
                # If bad boy wants to filter by not-in-model-field, he won't get result at all
            })

        conditions = []
        for key, value in filters.items():
            if '__' in key:
                field, operator = key.split('__', 1)
            else:
                field, operator = key, 'eq'

            if not hasattr(self.model, field):
                continue

            column = getattr(self.model, field)
            
            if operator == 'eq':
                conditions.append(column == value)
            elif operator == 'ne':
                conditions.append(column != value)
            elif operator == 'gt':
                conditions.append(column > value)
            elif operator == 'lt':
                conditions.append(column < value)
            elif operator == 'in':
                conditions.append(column.in_(value))
            elif operator == 'like':
                conditions.append(column.like(value))
        
        if conditions:
            self._query = self._query.where(and_(*conditions))
        return self

    def apply_join(self, *relationships: str) -> "PaginatorService":
        """
        Load relationships using joinedload
        Example: apply_join('posts', 'comments')
        """
        for rel in relationships:
            if hasattr(self.model, rel):
                self._query = self._query.options(joinedload(getattr(self.model, rel)))
        return self

    def apply_sort(self, sort_by: str, order: Literal["asc", "desc"] = "asc") -> "PaginatorService":
        """
        Apply sorting to the query.
        """
        if hasattr(self.model, sort_by):
            column = getattr(self.model, sort_by)
            self._query = self._query.order_by(asc(column) if order == "asc" else desc(column))
        return self

    async def get_page(
        self,
        page: int = 1,
        per_page: Optional[int] = None,
        **filters: Any
    ) -> PaginatorResult:
        """
        Retrieve a paginated page of results.
        """
        per_page = per_page or settings.PAGINATION_UNIT

        self.apply_filters(**filters)
        total_items = await self._count_total()

        total_pages = (total_items + per_page - 1) // per_page
        if page < 1 or (total_pages > 0 and page > total_pages):
            raise ValueError(f"Invalid page number: {page}. Valid range: 1-{total_pages}")

        offset = (page - 1) * per_page
        paginated_query = self._query.offset(offset).limit(per_page)

        result = await self.session.execute(paginated_query)
        items = result.unique().scalars().all() 

        return PaginatorResult(
            items=[self.item_model.model_validate(i.get_look()).model_dump() for i in items],
            page=page,
            total_pages=total_pages,
            total_items=total_items
        )

    async def _count_total(self) -> int:
        """Count total number of items matching the query."""
        count_query = select(func.count()).select_from(self.model)
        result = await self.session.execute(count_query)
        return result.scalar_one()