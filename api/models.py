from sqlalchemy import Column, String, Boolean, Float, \
Integer, DateTime, Table, ForeignKey, func, MetaData
from sqlalchemy.orm import mapped_column, relationship, DeclarativeBase
from datetime import datetime, UTC

from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.types import DateTime






metadata_obj = MetaData(schema=None)

class Base(DeclarativeBase):
    metadata = metadata_obj

recipe_tag = Table(
    "recipe_tag",
    Base.metadata,
    Column(
        "recipe_id", 
        ForeignKey("recipe.id"), 
        primary_key=True
    ),
    Column(
        "tag_id", 
        ForeignKey("tag.id"), 
        primary_key=True
    ),
)

complementary_dish = Table(
    "complementary_dish",
    Base.metadata,
    Column(
        "recipe_id", 
        ForeignKey("recipe.id"), 
        primary_key=True
    ),
    Column(
        "comp_recipe_id", 
        ForeignKey('recipe.id'), 
        primary_key=True
    ),
)

class Recipe(Base):
    __tablename__ = "recipe"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True, nullable=False)
    date_created = mapped_column(
        DateTime, default=datetime.now(UTC), nullable=False
    )
    date_modified = mapped_column(
        DateTime, default=None, onupdate=datetime.now(UTC)
    )
    created_by = mapped_column(
        Integer, 
        ForeignKey("user.id"),
        nullable=False,
    )
    modified_by = mapped_column(Integer, ForeignKey("user.id"))
    is_active = mapped_column(Boolean, default=True, nullable=False)

    directions = relationship(
        "Direction",
        lazy="select",
        order_by="Direction.order_id",
        cascade="all, delete-orphan",
    )

    tags = relationship(
       "Tag", 
       secondary=recipe_tag, 
       lazy="select",
       order_by="Tag.name"
    )

    complementary_dishes = relationship(
        "Recipe",
        secondary=complementary_dish,
        primaryjoin=(complementary_dish.c.recipe_id == id),
        secondaryjoin=(complementary_dish.c.comp_recipe_id == id),
        lazy="select"
    )

    def __repr__(self):
        return f"<Recipe {self.name}>"



class Tag(Base):
    __tablename__ = "tag"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True, nullable=False)
    is_active = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Tag {self.id} {self.name}>"

  
class Unit(Base):
    __tablename__ = "unit"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True, nullable=False)
    name_plural = mapped_column(String, unique=True, nullable=False)
    abbr_singular = mapped_column(String)
    abbr_plural = mapped_column(String)
    is_active = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Unit {self.id} {self.name}>"

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    user_name = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    role = mapped_column(String, nullable=False)
    is_active = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User {self.user_name}>"
    
class Direction(Base):
    __tablename__ = "direction"
    id = mapped_column(Integer, primary_key=True)
    recipe_id = mapped_column(
        Integer, 
        ForeignKey("recipe.id"),
        nullable=False,
    )
    order_id = mapped_column(Integer, nullable=False)
    description_ = mapped_column(String, nullable=False)

    ingredients = relationship(
        "Ingredient",
        lazy="joined",
        order_by="Ingredient.order_id",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Direction {self.recipe_id} {self.order_id}>"

class Ingredient(Base):
    __tablename__ = "ingredient"
    id = mapped_column(Integer, primary_key=True)
    direction_id = mapped_column(
        Integer, 
        ForeignKey("direction.id"),
        nullable=False
    )
    order_id = mapped_column(Integer, nullable=False)
    quantity = mapped_column(Float)
    unit_id = mapped_column(Integer, ForeignKey("unit.id"))
    item = mapped_column(String, nullable=False)

    unit = relationship(
        Unit,
        lazy="joined",
    )

    def __repr__(self):
        return f"<Ingredient {self.item}>"