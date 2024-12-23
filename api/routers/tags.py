from typing import Type, Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, func
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
)

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    # dependencies=[Depends(get_current_active_user)],
)


# tag endpoints
@router.get("/", response_model=list[schemas.TagSchema])
def read_tags(
    q: Annotated[str | None, Query(max_length=40)] = None,
    active_only: bool = False,
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):

    base_query = select(models.Tag).order_by(models.Tag.name)
    query = modify_query_for_activity(models.Tag, base_query, active_only)
    finished_query = modify_query_for_query_param(models.Tag, query, q)

    offset = (page - 1) * size
    finished_query = finished_query.offset(offset).limit(size)

    tag_orms = db.execute(finished_query).scalars().unique().all()

    return tag_orms


def generate_url_query(query_map: dict):
    return urlencode({k: v for k, v in query_map.items() if v is not None})


def generate_links(
    current_page: int,
    total_page_count: int,
    path: str,
    query_map: dict,
) -> dict:
    current = f"{path}?{generate_url_query(query_map)}"

    if current_page > 1:
        query_map.update(dict(page=current_page - 1))
        prev = f"{path}?{generate_url_query(query_map)}"
    else:
        prev = None

    if current_page < total_page_count:
        query_map.update(dict(page=current_page + 1))
        next = f"{path}?{generate_url_query(query_map)}"
    else:
        next = None

    return dict(
        current=current,
        prev=prev,
        next=next,
    )


@router.get("/page", response_model=schemas.TagPage)
def read_tag_page(
    pagination_input: PaginationDep,
    q: Annotated[str | None, Query(max_length=40)] = None,
    active_only: bool = False,
    db: Session = Depends(get_db),
):

    base_query = select(models.Tag).order_by(models.Tag.name)
    query = modify_query_for_activity(models.Tag, base_query, active_only)
    finished_query = modify_query_for_query_param(models.Tag, query, q)

    # get total count for given activity and query params
    total_row_count = db.execute(
        select(func.count(1).label("cnt")).select_from(finished_query.subquery())
    ).scalar_one()

    # calculate total page count
    total_page_count = (
        total_row_count // pagination_input.size + 1
        if total_row_count % pagination_input.size > 0
        else total_row_count // pagination_input.size
    )

    # give last page if requested page is out of bounds
    page = min(
        pagination_input.page,
        max(total_page_count, 1),  # give at least page 1 if no records
    )

    offset = (page - 1) * pagination_input.size
    finished_query = finished_query.offset(offset).limit(pagination_input.size)

    tag_orms = list(db.execute(finished_query).scalars().unique().all())

    page_output = schemas.TagPage(
        data=tag_orms,
        links=schemas.PageLinks(
            **generate_links(
                current_page=page,
                total_page_count=total_page_count,
                path="/tags/page",
                query_map=dict(
                    q=q, active_only=active_only, page=page, size=pagination_input.size
                ),
            )
        ),
    )

    return page_output


@router.get("/{id}", response_model=schemas.TagSchema)
def read_tag(id: int, active_only: bool = False, db: Session = Depends(get_db)):

    base_query = select(models.Tag).where(models.Tag.id == id)
    finished_query = modify_query_for_activity(models.Tag, base_query, active_only)

    tag_orm = db.execute(finished_query).unique().scalar_one_or_none()
    if not tag_orm:
        raise HTTPException(status_code=404, detail=f"Tag '{id}' not found")

    return tag_orm


@router.post("/", response_model=schemas.TagSchema, status_code=201)
def create_tag(tag_schema_input: schemas.TagCreate, db: Session = Depends(get_db)):

    # check for existing tag
    existing_tag = (
        db.execute(select(models.Tag).where(models.Tag.name == tag_schema_input.name))
        .unique()
        .scalar_one_or_none()
    )
    if existing_tag:
        raise HTTPException(
            status_code=409,
            detail=f"Tag '{tag_schema_input.name}' with id '{existing_tag.id}' already exists",
        )

    # create model instance
    tag_orm = models.Tag(**tag_schema_input.model_dump())

    # update db
    db.add(tag_orm)
    db.commit()
    db.refresh(tag_orm)

    return tag_orm


@router.put("/{id}", response_model=schemas.TagSchema)
def update_tag(
    id: int, tag_schema_input: schemas.TagEdit, db: Session = Depends(get_db)
):

    # check for existing tag
    existing_tag = (
        db.execute(select(models.Tag).where(models.Tag.id == id))
        .unique()
        .scalar_one_or_none()
    )
    if not existing_tag:
        raise HTTPException(status_code=404, detail=f"Tag '{id}' does not exist")

    # check input schema tag name doesn't already exist on another record
    if existing_tag.name != tag_schema_input.name:
        conflicting_tag = (
            db.execute(
                select(models.Tag).where(models.Tag.name == tag_schema_input.name)
            )
            .unique()
            .scalar_one_or_none()
        )
        if conflicting_tag:
            raise HTTPException(
                status_code=400,
                detail=f"Tag '{tag_schema_input.name}' with id '{conflicting_tag.id}' already exists. Cannot update tag '{id}'.",
            )

    # # create model instance
    # tag_orm_new = models.Tag(id=id, **tag_schema_input.model_dump())

    # # update attributes on existing tag
    # for key in tag_orm_new.__mapper__.attrs.keys():
    #   setattr(existing_tag, key, getattr(tag_orm_new, key))
    for key, value in tag_schema_input.model_dump().items():
        setattr(existing_tag, key, value)

    # update db
    db.commit()
    db.refresh(existing_tag)

    return existing_tag


@router.delete("/{id}", response_model=schemas.TagSchema)
def delete_tag(id: int, db: Session = Depends(get_db)):

    # check for existing tag
    existing_tag = (
        db.execute(
            select(models.Tag)
            .where(models.Tag.is_active == True)
            .where(models.Tag.id == id)
        )
        .unique()
        .scalar_one_or_none()
    )
    if not existing_tag:
        raise HTTPException(status_code=404, detail=f"Tag '{id}' does not exist")

    # make existing tag inactive
    existing_tag.is_active = False

    # update db
    db.commit()
    db.refresh(existing_tag)

    return existing_tag
