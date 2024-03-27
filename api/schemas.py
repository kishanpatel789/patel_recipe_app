from pydantic import BaseModel, ConfigDict, HttpUrl, constr
from typing import Optional, List
from datetime import datetime

class MyBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
    )

class TagBase(MyBaseModel):
    name: constr(min_length=1)

class TagCreate(TagBase):
    pass

class TagSchema(TagBase):
    id: int
