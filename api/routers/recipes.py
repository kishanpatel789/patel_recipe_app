from datetime import datetime, UTC
from typing import Type, Optional, Annotated

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy import select, or_
from sqlalchemy.orm import Session  # for typing
from sqlalchemy.sql.selectable import Select  # for typing
from sqlalchemy.ext.declarative import DeclarativeMeta

from .. import models, schemas
from ..database import get_db
from ..auth import get_current_active_user
from .common import (
    modify_query_for_activity,
    modify_query_for_query_param,
    PaginationDep,
    QueryDep,
    paginate,
)

router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    # dependencies=[Depends(get_current_active_user)],
)


def verify_unit_id(unit_id: int | None, db: Session):
    if unit_id is None:
        pass
    else:
        existing_unit = (
            db.execute(
                select(models.Unit)
                .where(models.Unit.id == unit_id)
                .where(models.Unit.is_active == True)
            )
            .unique()
            .scalar_one_or_none()
        )
        if existing_unit is None:
            raise HTTPException(
                status_code=409,
                detail=f"Unit ID '{unit_id}' does not exist or is inactive.",
            )


# endpoints
@router.get("/", response_model=schemas.RecipePage)
def read_recipes(
    pagination_input: PaginationDep,
    request: Request,
    q: QueryDep,
    active_only: bool = False,
    db: Session = Depends(get_db),
):

    base_query = select(models.Recipe).order_by(models.Recipe.name)
    query = modify_query_for_activity(models.Recipe, base_query, active_only)
    finished_query = modify_query_for_query_param(models.Recipe, query, q)

    query_params = dict(q=q, active_only=active_only)
    data, links = paginate(
        pagination_input=pagination_input,
        request=request,
        query_params=query_params,
        query=finished_query,
        db=db,
    )

    page_output = schemas.RecipePage(data=data, links=links)

    return page_output


@router.get("/id/{id}", response_model=schemas.RecipeDetailSchema)
def read_recipe_by_id(
    id: int, active_only: bool = False, db: Session = Depends(get_db)
):

    base_query = select(models.Recipe).where(models.Recipe.id == id)
    finished_query = modify_query_for_activity(models.Recipe, base_query, active_only)

    recipe_orm = db.execute(finished_query).unique().scalar_one_or_none()
    if recipe_orm is None:
        raise HTTPException(status_code=404, detail=f"Recipe '{id}' not found")

    return recipe_orm


@router.get("/slug/{slug}", response_model=schemas.RecipeDetailSchema)
def read_recipe_by_slug(
    slug: str, active_only: bool = False, db: Session = Depends(get_db)
):

    base_query = select(models.Recipe).where(models.Recipe.slug == slug)
    finished_query = modify_query_for_activity(models.Recipe, base_query, active_only)

    recipe_orm = db.execute(finished_query).unique().scalar_one_or_none()
    if recipe_orm is None:
        raise HTTPException(status_code=404, detail=f"Recipe '{slug}' not found")

    return recipe_orm


@router.post("/", response_model=schemas.RecipeDetailSchema, status_code=201)
def create_recipe(
    recipe_schema_input: schemas.RecipeCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserDetailSchema = Depends(get_current_active_user),
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
                created_by=current_user.id,
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
                    verify_unit_id(ingredient.unit_id, db)

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


@router.put("/{id}", response_model=schemas.RecipeDetailSchema)
def update_recipe(
    id: int,
    recipe_schema_input: schemas.RecipeEdit,
    db: Session = Depends(get_db),
    current_user: schemas.UserDetailSchema = Depends(get_current_active_user),
):

    # check for existing recipe
    existing_recipe = (
        db.execute(select(models.Recipe).where(models.Recipe.id == id))
        .unique()
        .scalar_one_or_none()
    )
    if existing_recipe is None:
        raise HTTPException(status_code=404, detail=f"Recipe '{id}' does not exist")

    # check input schema recipe name doesn't already exist on another record
    if existing_recipe.name != recipe_schema_input.name:
        conflicting_recipe = (
            db.execute(
                select(models.Recipe).where(
                    models.Recipe.name == recipe_schema_input.name
                )
            )
            .unique()
            .scalar_one_or_none()
        )
        if conflicting_recipe:
            raise HTTPException(
                status_code=400,
                detail=f"Recipe '{recipe_schema_input.name}' with id '{conflicting_recipe.id}' already exists. Cannot update slug '{id}'.",
            )

    # check input schema recipe slug doesn't already exist on another record
    if existing_recipe.slug != recipe_schema_input.slug:
        conflicting_recipe = (
            db.execute(
                select(models.Recipe).where(
                    models.Recipe.slug == recipe_schema_input.slug
                )
            )
            .unique()
            .scalar_one_or_none()
        )
        if conflicting_recipe:
            raise HTTPException(
                status_code=400,
                detail=f"Recipe '{recipe_schema_input.slug}' with id '{conflicting_recipe.id}' already exists. Cannot update slug '{id}'.",
            )

    try:
        db.close()  # close session to handle transactional-level management
        with db.begin():

            # update recipe model
            existing_recipe = (
                db.execute(select(models.Recipe).where(models.Recipe.id == id))
                .unique()
                .scalar_one()
            )
            existing_recipe.name = recipe_schema_input.name
            existing_recipe.slug = recipe_schema_input.slug
            existing_recipe.date_modified = datetime.now(UTC)
            existing_recipe.modified_by = current_user.id
            existing_recipe.is_active = recipe_schema_input.is_active

            # update direction model - create, update, delete
            # get existing directions
            existing_directions = (
                db.execute(
                    select(models.Direction)
                    .where(models.Direction.recipe_id == id)
                    .order_by(models.Direction.order_id)
                )
                .scalars()
                .unique()
                .all()
            )
            existing_direction_cnt = len(existing_directions)
            new_direction_cnt = len(recipe_schema_input.directions)

            for input_direction_index, input_direction in enumerate(
                recipe_schema_input.directions
            ):
                if input_direction_index < existing_direction_cnt:
                    # update direction
                    existing_direction = existing_directions[input_direction_index]
                    existing_direction.description_ = input_direction.description_

                    # get existing ingredients
                    existing_ingredients = (
                        db.execute(
                            select(models.Ingredient)
                            .where(
                                models.Ingredient.direction_id == existing_direction.id
                            )
                            .order_by(models.Ingredient.order_id)
                        )
                        .scalars()
                        .unique()
                        .all()
                    )
                    existing_ingredient_cnt = len(existing_ingredients)
                    new_ingredient_cnt = len(input_direction.ingredients)
                    new_ingredients = []

                    for input_ingredient_index, input_ingredient in enumerate(
                        input_direction.ingredients
                    ):
                        verify_unit_id(input_ingredient.unit_id, db)

                        if input_ingredient_index < existing_ingredient_cnt:
                            # update ingredient for existing direction
                            existing_ingredient = existing_ingredients[
                                input_ingredient_index
                            ]
                            existing_ingredient.quantity = input_ingredient.quantity
                            existing_ingredient.unit_id = input_ingredient.unit_id
                            existing_ingredient.item = input_ingredient.item
                        else:
                            # create ingredient for existing direction
                            new_ingredient = models.Ingredient(
                                direction_id=existing_direction.id,
                                order_id=input_ingredient_index + 1,
                                quantity=input_ingredient.quantity,
                                unit_id=input_ingredient.unit_id,
                                item=input_ingredient.item,
                            )
                            new_ingredients.append(new_ingredient)
                    db.add_all(new_ingredients)

                    # delete ingredient for existing direction
                    if new_ingredient_cnt < existing_ingredient_cnt:
                        for i in range(new_ingredient_cnt, existing_ingredient_cnt):
                            db.delete(existing_ingredients[i])
                else:
                    # create direction
                    new_direction = models.Direction(
                        recipe_id=id,
                        order_id=input_direction_index + 1,
                        description_=input_direction.description_,
                    )
                    db.add(new_direction)
                    db.flush()

                    # create ingredients for new direction
                    new_ingredients = []
                    for input_ingredient_index, input_ingredient in enumerate(
                        input_direction.ingredients
                    ):
                        verify_unit_id(input_ingredient.unit_id, db)

                        new_ingredient = models.Ingredient(
                            direction_id=new_direction.id,
                            order_id=input_ingredient_index + 1,
                            quantity=input_ingredient.quantity,
                            unit_id=input_ingredient.unit_id,
                            item=input_ingredient.item,
                        )
                        new_ingredients.append(new_ingredient)
                    db.add_all(new_ingredients)

            # delete direction
            if new_direction_cnt < existing_direction_cnt:
                for i in range(new_direction_cnt, existing_direction_cnt):
                    db.delete(existing_directions[i])
    except Exception as e:
        print(e)
        raise

    db.refresh(existing_recipe)

    return existing_recipe


@router.delete("/{id}", response_model=schemas.RecipeDetailSchema)
def delete_recipe(id: int, db: Session = Depends(get_db)):

    # check for existing recipe
    existing_recipe = (
        db.execute(
            select(models.Recipe)
            .where(models.Recipe.is_active == True)
            .where(models.Recipe.id == id)
        )
        .unique()
        .scalar_one_or_none()
    )
    if existing_recipe is None:
        raise HTTPException(status_code=404, detail=f"Recipe '{id}' does not exist")

    # make existing recipe inactive
    existing_recipe.is_active = False
    existing_recipe.date_modified = datetime.now(UTC)
    existing_recipe.modified_by = 2

    # update db
    db.commit()
    db.refresh(existing_recipe)

    return existing_recipe
