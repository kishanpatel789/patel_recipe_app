from typing import Type, Protocol, Annotated

from sqlalchemy.sql.selectable import Select  # for typing
from sqlalchemy.orm import MappedColumn
from fastapi import Depends

from ..models import IsActiveMixin
from ..schemas import PaginationInput


class ModelWithName(Protocol):
    name: MappedColumn


# helper functions
def modify_query_for_activity(
    model: Type[IsActiveMixin], query: Select, active_only: bool
):
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
):
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

PaginationDep = Annotated[PaginationInput, Depends()]