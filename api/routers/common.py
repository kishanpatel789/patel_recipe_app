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
