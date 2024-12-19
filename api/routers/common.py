from sqlalchemy.sql.selectable import Select  # for typing
from sqlalchemy.orm import DeclarativeBase
from typing import Type


# helper functions
def modify_query_for_activity(
    model: Type[DeclarativeBase], query: Select, active_only: bool
):
    if active_only:
        return query.where(model.is_active == True)
    else:
        return query


def modify_query_for_query_param(
    model: Type[DeclarativeBase], query: Select, query_param: str | None
):
    if query_param:
        return query.where(
            model.name.ilike(f"%{query_param.strip().replace(' ', '%')}%")
        )
    else:
        return query
