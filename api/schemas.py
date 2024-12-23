from pydantic import BaseModel, Field, ConfigDict, HttpUrl, constr, PositiveFloat
from datetime import datetime


class MyBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,
        str_min_length=1,
    )


class PaginationInput(MyBaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=50)


class PageLinks(MyBaseModel):
    current: HttpUrl
    prev: HttpUrl | None = None
    next: HttpUrl | None = None


class PageBase(MyBaseModel):
    data: list
    links: PageLinks


class TagBase(MyBaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagEdit(TagBase):
    is_active: bool


class TagSchema(TagEdit):
    id: int


class TagPage(PageBase):
    data: list[TagSchema]


class UnitBase(MyBaseModel):
    name: str
    name_plural: str
    abbr_singular: str | None
    abbr_plural: str | None


class UnitCreate(UnitBase):
    pass


class UnitEdit(UnitBase):
    is_active: bool


class UnitSchema(UnitBase):
    id: int


class UnitDetailSchema(UnitEdit):
    id: int


class UnitPage(PageBase):
    data: list[UnitSchema]


class IngredientBase(MyBaseModel):
    quantity: PositiveFloat | None = None
    unit: UnitBase | None = None
    item: str


class IngredientCreate(MyBaseModel):
    quantity: PositiveFloat | None = None
    unit_id: int | None = None
    item: str


class IngredientSchema(IngredientBase):
    id: int
    unit: UnitSchema | None = None


class DirectionBase(MyBaseModel):
    description_: str
    ingredients: list[IngredientBase]


class DirectionCreate(MyBaseModel):
    description_: str
    ingredients: list[IngredientCreate]


class DirectionSchema(DirectionBase):
    id: int
    ingredients: list[IngredientSchema]


class RecipeBase(MyBaseModel):
    name: str
    slug: str


class RecipeCreate(RecipeBase):
    directions: list[DirectionCreate]


class RecipeEdit(RecipeCreate):
    is_active: bool


class RecipeSchema(RecipeBase):
    id: int
    date_created: datetime
    date_modified: datetime | None = None
    created_by: int
    modified_by: int | None = None
    is_active: bool


class RecipeDetailSchema(RecipeSchema):
    directions: list[DirectionSchema]


class RecipePage(PageBase):
    data: list[RecipeSchema]


class UserBase(MyBaseModel):
    user_name: str
    role: str


class UserSchema(UserBase):
    id: int
    is_active: bool


class UserDetailSchema(UserSchema):
    hashed_password: str
