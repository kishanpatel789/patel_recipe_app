from pydantic import BaseModel, ConfigDict, HttpUrl, constr
from typing import Optional, List
from datetime import datetime


class MyBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        str_min_length=1,
    )


class TagBase(MyBaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagEdit(TagBase):
    is_active: bool


class TagSchema(TagEdit):
    id: int


class UnitBase(MyBaseModel):
    name: str
    name_plural: str
    abbr_singular: str | None
    abbr_plural: str | None


class UnitCreate(UnitBase):
    pass


class UnitEdit(UnitBase):
    is_active: bool


class UnitSchema(UnitEdit):
    id: int

class IngredientBase(MyBaseModel):
    quantity: float
    unit: UnitBase
    item: str

class DirectionBase(MyBaseModel):
    description_: str
    ingredients: List[IngredientBase]


class RecipeBase(MyBaseModel):
    name: str
    slug: str


# class RecipeCreate(RecipeBase):
#     pass


class RecipeEdit(RecipeBase):
    is_active: bool


class RecipeSchema(RecipeEdit):
    id: int
    date_created: datetime
    date_modified: datetime | None
    created_by: int
    modified_by: int | None

class RecipeDetailSchema(RecipeSchema):
    directions: List[DirectionBase]

