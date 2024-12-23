from typing import Type, Protocol, Annotated
from urllib.parse import urlencode

from sqlalchemy import select, func
from sqlalchemy.sql.selectable import Select  # for typing
from sqlalchemy.orm import MappedColumn, Session
from fastapi import Depends, Request
from pydantic import HttpUrl

from .. import models
from .. import schemas


class ModelWithName(Protocol):
    name: MappedColumn


# helper functions
def modify_query_for_activity(
    model: Type[models.IsActiveMixin], query: Select, active_only: bool
) -> Select:
    if active_only is not None:
        if hasattr(model, "is_active"):
            return query.where(model.is_active == True)
        else:
            raise AttributeError(
                f"Model '{model.__name__}' does not have an 'is_active' attribute"
            )
    else:
        return query


def modify_query_for_query_param(
    model: Type[ModelWithName], query: Select, query_param: str | None
) -> Select:
    if query_param is not None:
        if hasattr(model, "name"):
            return query.where(
                model.name.ilike(f"%{query_param.strip().replace(' ', '%')}%")
            )
        else:
            raise AttributeError(
                f"Model '{model.__name__}' does not have a 'name' attribute"
            )
    else:
        return query


def generate_url_query(query_map: dict):
    return urlencode({k: v for k, v in query_map.items() if v is not None})


def generate_links(
    current_page: int,
    total_page_count: int,
    request: Request,
    query_map: dict,

) -> schemas.PageLinks:
    
    base_url = f"{request.url.scheme}://{request.url.netloc}{request.url.path}"

    current = f"{base_url}?{generate_url_query(query_map)}"

    if current_page > 1:
        query_map.update(dict(page=current_page - 1))
        prev = f"{base_url}?{generate_url_query(query_map)}"
    else:
        prev = None

    if current_page < total_page_count:
        query_map.update(dict(page=current_page + 1))
        next = f"{base_url}?{generate_url_query(query_map)}"
    else:
        next = None

    return schemas.PageLinks(
        current=current, # type: ignore
        prev=prev, # type: ignore
        next=next, # type: ignore
    )


def paginate(
    pagination_input: schemas.PaginationInput,
    request: Request,
    query_params: dict,
    query: Select,
    db: Session,
) -> tuple[list, schemas.PageLinks]:
    
    # get total count for given activity and query params
    total_row_count = db.execute(
        select(func.count(1).label("cnt")).select_from(query.subquery())
    ).scalar_one()

    # calculate total page count
    total_page_count = (
        total_row_count // pagination_input.size + 1
        if total_row_count % pagination_input.size > 0
        else total_row_count // pagination_input.size
    )

    # give last page if requested page is out of bounds
    page = min(
        pagination_input.page,
        max(total_page_count, 1),  # give at least page 1 if no records
    )
    query_params.update(dict(page=page, size=pagination_input.size))

    offset = (page - 1) * pagination_input.size
    finished_query = query.offset(offset).limit(pagination_input.size)
    
    data = list(db.execute(finished_query).scalars().unique().all())

    links = generate_links(
        current_page=page,
        total_page_count=total_page_count,
        request=request,
        query_map=query_params,
    )

    return data, links


PaginationDep = Annotated[schemas.PaginationInput, Depends()]
