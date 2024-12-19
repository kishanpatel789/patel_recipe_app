from typing import Type, Protocol

from sqlalchemy.sql.selectable import Select  # for typing
from sqlalchemy.orm import MappedColumn

from ..models import IsActiveMixin


class ModelWithName(Protocol):
    name: MappedColumn


# helper functions
def modify_query_for_activity(
    model: Type[IsActiveMixin], query: Select, active_only: bool
):
    if active_only:
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
    if query_param:
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
