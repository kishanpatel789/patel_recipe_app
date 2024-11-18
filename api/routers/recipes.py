from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy import select, or_
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
def read_recipe_by_id(
    id: int, active_only: bool = False, db: Session = Depends(get_db)
):

    base_query = select(models.Recipe).where(models.Recipe.id == id)
    finished_query = modify_query_for_activity(models.Recipe, base_query, active_only)

    recipe_orm = db.execute(finished_query).unique().scalar_one_or_none()
    if not recipe_orm:
        raise HTTPException(status_code=404, detail=f"Recipe '{id}' not found")

    return recipe_orm


@router.get("/slug/{slug}", response_model=schemas.RecipeDetailSchema)
def read_recipe_by_slug(
    slug: str, active_only: bool = False, db: Session = Depends(get_db)
):

    base_query = select(models.Recipe).where(models.Recipe.slug == slug)
    finished_query = modify_query_for_activity(models.Recipe, base_query, active_only)

    recipe_orm = db.execute(finished_query).unique().scalar_one_or_none()
    if not recipe_orm:
        raise HTTPException(status_code=404, detail=f"Recipe '{slug}' not found")

    return recipe_orm


@router.post("/", response_model=schemas.RecipeDetailSchema, status_code=201)
def create_recipe(
    recipe_schema_input: schemas.RecipeCreate, db: Session = Depends(get_db)
):

    # check for existing recipe
    existing_recipe = (
        db.execute(
            select(models.Recipe).where(
                or_(
                    models.Recipe.name == recipe_schema_input.name,
                    models.Recipe.slug == recipe_schema_input.slug,
                )
            )
        )
        .unique()
        .scalar_one_or_none()
    )

    if existing_recipe:
        raise HTTPException(
            status_code=409,
            detail=f"Recipe '{recipe_schema_input.name}' with slug '{existing_recipe.slug}' and id '{existing_recipe.id}' already exists",
        )

    try:
        db.close()  # close session to handle transactional-level management
        with db.begin():
            # create recipe model
            recipe_orm = models.Recipe(
                name=recipe_schema_input.name,
                slug=recipe_schema_input.slug,
                created_by=1,  # TODO: remove hard-code with logged in user
            )
            db.add(recipe_orm)
            db.flush()

            # create direction model
            for i, direction in enumerate(recipe_schema_input.directions):
                direction_orm = models.Direction(
                    recipe_id=recipe_orm.id,
                    order_id=i + 1,
                    description_=direction.description_,
                )
                db.add(direction_orm)
                db.flush()

                # process ingredients
                for j, ingredient in enumerate(direction.ingredients):
                    # verify unit id
                    existing_unit = (
                        db.execute(
                            select(models.Unit).where(
                                models.Unit.id == ingredient.unit_id,
                            )
                        )
                        .unique()
                        .scalar_one_or_none()
                    )
                    if existing_unit == None:
                        raise HTTPException(
                            status_code=409,
                            detail=f"Unit ID '{ingredient.unit_id}' does not exist. Referenced in direction '{i}', ingredient '{j}' '{ingredient.item}'",
                        )

                    # create ingredient model
                    ingredient_orm = models.Ingredient(
                        direction_id=direction_orm.id,
                        order_id=j + 1,
                        quantity=ingredient.quantity,
                        unit_id=ingredient.unit_id,
                        item=ingredient.item,
                    )
                    db.add(ingredient_orm)

    except Exception as e:
        print(e)
        raise

    db.refresh(recipe_orm)

    return recipe_orm


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
