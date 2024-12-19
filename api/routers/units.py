from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session  # for typing

from .. import models, schemas
from ..database import get_db
from ..auth import get_current_active_user
from .common import modify_query_for_activity, modify_query_for_query_param

router = APIRouter(
    prefix="/units",
    tags=["units"],
    dependencies=[Depends(get_current_active_user)],
)


# unit endpoints
@router.get("/", response_model=list[schemas.UnitDetailSchema])
def read_units(
    q: Annotated[str | None, Query(max_length=40)] = None,
    active_only: bool = False,
    db: Session = Depends(get_db),
):

    base_query = select(models.Unit).order_by(models.Unit.name)
    query = modify_query_for_activity(models.Unit, base_query, active_only)
    finished_query = modify_query_for_query_param(models.Unit, query, q)

    unit_orms = db.execute(finished_query).scalars().unique().all()

    return unit_orms


@router.get("/{id}", response_model=schemas.UnitDetailSchema)
def read_unit(id: int, active_only: bool = False, db: Session = Depends(get_db)):

    base_query = select(models.Unit).where(models.Unit.id == id)
    finished_query = modify_query_for_activity(models.Unit, base_query, active_only)

    unit_orm = db.execute(finished_query).unique().scalar_one_or_none()
    if not unit_orm:
        raise HTTPException(status_code=404, detail=f"Unit '{id}' not found")

    return unit_orm


@router.post("/", response_model=schemas.UnitDetailSchema, status_code=201)
def create_unit(unit_schema_input: schemas.UnitCreate, db: Session = Depends(get_db)):

    # check for existing record
    existing_unit = (
        db.execute(
            select(models.Unit).where(models.Unit.name == unit_schema_input.name)
        )
        .unique()
        .scalar_one_or_none()
    )
    if existing_unit:
        raise HTTPException(
            status_code=409,
            detail=f"Unit '{unit_schema_input.name}' with id '{existing_unit.id}' already exists",
        )

    # create model instance
    unit_orm = models.Unit(**unit_schema_input.model_dump())

    # update db
    db.add(unit_orm)
    db.commit()
    db.refresh(unit_orm)

    return unit_orm


@router.put("/{id}", response_model=schemas.UnitDetailSchema)
def update_unit(
    id: int, unit_schema_input: schemas.UnitEdit, db: Session = Depends(get_db)
):

    # check for existing record
    existing_unit = (
        db.execute(select(models.Unit).where(models.Unit.id == id))
        .unique()
        .scalar_one_or_none()
    )
    if not existing_unit:
        raise HTTPException(status_code=404, detail=f"Unit '{id}' does not exist")

    # check input schema unit name doesn't already exist on another record
    if existing_unit.name != unit_schema_input.name:
        conflicting_unit = (
            db.execute(
                select(models.Unit).where(models.Unit.name == unit_schema_input.name)
            )
            .unique()
            .scalar_one_or_none()
        )
        if conflicting_unit:
            raise HTTPException(
                status_code=400,
                detail=f"Tag '{unit_schema_input.name}' with id '{conflicting_unit.id}' already exists. Cannot update tag '{id}'.",
            )

    for key, value in unit_schema_input.model_dump().items():
        setattr(existing_unit, key, value)

    # update db
    db.commit()
    db.refresh(existing_unit)

    return existing_unit


@router.delete("/{id}", response_model=schemas.UnitDetailSchema)
def delete_unit(id: int, db: Session = Depends(get_db)):

    # check for existing record
    existing_unit = (
        db.execute(
            select(models.Unit)
            .where(models.Unit.is_active == True)
            .where(models.Unit.id == id)
        )
        .unique()
        .scalar_one_or_none()
    )
    if not existing_unit:
        raise HTTPException(status_code=404, detail=f"Unit '{id}' does not exist")

    # make existing tag inactive
    existing_unit.is_active = False

    # update db
    db.commit()
    db.refresh(existing_unit)

    return existing_unit
