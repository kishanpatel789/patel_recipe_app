from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session  # for typing
from sqlalchemy.sql.selectable import Select  # for typing
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Type, Optional

from .. import models, schemas
from ..database import get_db
from .common import modify_query_for_activity

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)


# endpoints
@router.get("/", response_model=list[schemas.RecipeSchema])
def read_recipes(active_only: bool = False, db: Session = Depends(get_db)):

    base_query = select(models.Recipe).order_by(models.Recipe.name)
    finished_query = modify_query_for_activity(models.Recipe, base_query, active_only)

    recipe_orms = db.execute(finished_query).scalars().unique().all()

    return recipe_orms


@router.get("/id/{id}", response_model=schemas.RecipeDetailSchema)
def read_recipe(id: int, active_only: bool = False, db: Session = Depends(get_db)):

    base_query = select(models.Recipe).where(models.Recipe.id == id)
    finished_query = modify_query_for_activity(models.Recipe, base_query, active_only)

    recipe_orm = db.execute(finished_query).unique().scalar_one_or_none()
    if not recipe_orm:
        raise HTTPException(status_code=404, detail=f"Recipe '{id}' not found")

    return recipe_orm


# @router.post("/", response_model=schemas.RecipeSchema, status_code=201)
# def create_tag(tag_schema_input: schemas.TagCreate, db: Session = Depends(get_db)):

#     # check for existing tag
#     existing_tag = (
#         db.execute(select(models.Recipe).where(models.Recipe.name == tag_schema_input.name))
#         .unique()
#         .scalar_one_or_none()
#     )
#     if existing_tag:
#         raise HTTPException(
#             status_code=409,
#             detail=f"Tag '{tag_schema_input.name}' with id '{existing_tag.id}' already exists",
#         )

#     # create model instance
#     tag_orm = models.Recipe(**tag_schema_input.model_dump())

#     # update db
#     db.add(tag_orm)
#     db.commit()
#     db.refresh(tag_orm)

#     return tag_orm


# @router.put("/{id}", response_model=schemas.RecipeSchema)
# def update_tag(
#     id: int, tag_schema_input: schemas.TagEdit, db: Session = Depends(get_db)
# ):

#     # check for existing tag
#     existing_tag = (
#         db.execute(select(models.Recipe).where(models.Recipe.id == id))
#         .unique()
#         .scalar_one_or_none()
#     )
#     if not existing_tag:
#         raise HTTPException(status_code=404, detail=f"Tag '{id}' does not exist")

#     # check input schema tag name doesn't already exist on another record
#     if existing_tag.name != tag_schema_input.name:
#         conflicting_tag = (
#             db.execute(
#                 select(models.Recipe).where(models.Recipe.name == tag_schema_input.name)
#             )
#             .unique()
#             .scalar_one_or_none()
#         )
#         if conflicting_tag:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Tag '{tag_schema_input.name}' with id '{conflicting_tag.id}' already exists. Cannot update tag '{id}'.",
#             )

#     # # create model instance
#     # tag_orm_new = models.Recipe(id=id, **tag_schema_input.model_dump())

#     # # update attributes on existing tag
#     # for key in tag_orm_new.__mapper__.attrs.keys():
#     #   setattr(existing_tag, key, getattr(tag_orm_new, key))
#     for key, value in tag_schema_input.model_dump().items():
#         setattr(existing_tag, key, value)

#     # update db
#     db.commit()
#     db.refresh(existing_tag)

#     return existing_tag


# @router.delete("/{id}", response_model=schemas.RecipeSchema)
# def delete_tag(id: int, db: Session = Depends(get_db)):

#     # check for existing tag
#     existing_tag = (
#         db.execute(
#             select(models.Recipe)
#             .where(models.Recipe.is_active == True)
#             .where(models.Recipe.id == id)
#         )
#         .unique()
#         .scalar_one_or_none()
#     )
#     if not existing_tag:
#         raise HTTPException(status_code=404, detail=f"Tag '{id}' does not exist")

#     # make existing tag inactive
#     existing_tag.is_active = False

#     # update db
#     db.commit()
#     db.refresh(existing_tag)

#     return existing_tag
