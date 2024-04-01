from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session  # for typing

from .. import models, schemas
from ..database import get_db

router = APIRouter(
  prefix="/tags",
  tags=["tags"],
)

# tag endpoints
@router.get("/", response_model=list[schemas.TagSchema])
def read_tags(db: Session = Depends(get_db)):
  tag_orms = db.execute(
    select(models.Tag).order_by(models.Tag.name)
  ).scalars().unique().all()

  return tag_orms

@router.get("/{id}", response_model=schemas.TagSchema)
def read_tag(id: int, db: Session = Depends(get_db)):

  tag_orm = db.execute(
    select(models.Tag).filter(models.Tag.id == id)
  ).unique().scalar_one_or_none()
  if not tag_orm:
    raise HTTPException(status_code=404, detail=f"Tag '{id}' not found")
  
  return tag_orm

@router.post("/", response_model=schemas.TagSchema, status_code=201)
def create_tag(tag_schema_input: schemas.TagCreate, db: Session = Depends(get_db)):
  
  # check for existing tag
  existing_tag = db.execute(
    select(models.Tag).filter(models.Tag.name == tag_schema_input.name)
  ).unique().scalar_one_or_none()
  if existing_tag:
    raise HTTPException(status_code=409, detail=f"Tag '{tag_schema_input.name}' with id '{existing_tag.id}' already exists")
  
  # create model instance
  tag_orm = models.Tag(**tag_schema_input.model_dump())

  # update db
  db.add(tag_orm)
  db.commit()
  db.refresh(tag_orm)

  return tag_orm

@router.put("/{id}", response_model=schemas.TagSchema)
def update_tag(id: int, tag_schema_input: schemas.TagCreate, db: Session = Depends(get_db)):
  
  # check for existing tag
  existing_tag = db.execute(
    select(models.Tag).filter(models.Tag.id == id)
  ).unique().scalar_one_or_none()
  if not existing_tag:
    raise HTTPException(status_code=404, detail=f"Tag '{id}' does not exist")
  
  # check input schema tag name doesn't already exist on another record
  if existing_tag.name != tag_schema_input.name:
    conflicting_tag = db.execute(
      select(models.Tag).filter(models.Tag.name == tag_schema_input.name)
    ).unique().scalar_one_or_none()
    if conflicting_tag:
      raise HTTPException(status_code=400, detail=f"Tag '{tag_schema_input.name}' with id '{conflicting_tag.id}' already exists. Cannot update tag '{id}'.")

  # update attributes on existing tag
  existing_tag.name = tag_schema_input.name

  # update db
  db.commit()
  db.refresh(existing_tag)

  return existing_tag