from sqlalchemy import Column, String, Boolean, \
Integer, DateTime, Table, ForeignKey, func, MetaData
from sqlalchemy.orm import mapped_column, relationship, DeclarativeBase
from datetime import datetime

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime






metadata_obj = MetaData(schema=None)

class Base(DeclarativeBase):
    metadata = metadata_obj

class Tag(Base):
    __tablename__ = "tag"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag {self.id} {self.name}>"

  

