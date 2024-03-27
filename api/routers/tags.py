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
@router.get("/", response_model=list[schemas.TagBase])
def read_tags(db: Session = Depends(get_db)):
  tag_orms = db.execute(
    select(models.Tag).order_by(models.Tag.name)
  ).scalars().unique().all()

  return tag_orms