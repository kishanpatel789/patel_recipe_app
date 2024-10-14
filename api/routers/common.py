from sqlalchemy.sql.selectable import Select  # for typing
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Type


# helper functions
def modify_query_for_activity(
    model: Type[DeclarativeMeta], query: Select, active_only: bool
):
    if active_only:
        return query.where(model.is_active == True)
    else:
        return query
