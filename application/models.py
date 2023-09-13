from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

recipe_tag = db.Table(
    "recipe_tag",
    db.Column("recipe_id", db.ForeignKey("recipe.id"), primary_key=True),
    db.Column("tag_id", db.ForeignKey("tag.id"), primary_key=True),
)

complementary_dish = db.Table(
    "complementary_dish",
    db.Column("recipe_id", db.ForeignKey("recipe.id"), primary_key=True),
    db.Column("comp_recipe_id", db.ForeignKey('recipe.id'), primary_key=True),
)

class Recipe(db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    date_created = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False
    )
    date_modified = db.Column(
        db.DateTime, default=None, onupdate=datetime.utcnow
    )
    created_by = db.Column(db.Integer, 
                           db.ForeignKey("user.id"),
                           nullable=False,
    )
    modified_by = db.Column(db.Integer, db.ForeignKey("user.id"))

    directions = db.relationship(
        "Direction",
        lazy="select",
        order_by="Direction.order_id",
    )

    tags = db.relationship(
       "Tag", 
       secondary=recipe_tag, 
       lazy="select",
    )

    complementary_dishes = db.relationship(
        "Recipe",
        secondary=complementary_dish,
        primaryjoin=(complementary_dish.c.recipe_id == id),
        secondaryjoin=(complementary_dish.c.comp_recipe_id == id),
        lazy="select"
    )

    def __repr__(self):
        return f"<Recipe {self.name}>"


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User {self.user_name}>"

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag {self.id} {self.name}>"

class Unit(db.Model):
    __tablename__ = "unit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    name_plural = db.Column(db.String, unique=True, nullable=False)
    abbr_singular = db.Column(db.String)
    abbr_plural = db.Column(db.String)

    def __repr__(self):
        return f"<Unit {self.id} {self.name}>"

class Direction(db.Model):
    __tablename__ = "direction"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(
        db.Integer, 
        db.ForeignKey("recipe.id"),
        nullable=False,
    )
    order_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)

    ingredients = db.relationship(
        "Ingredient",
        lazy="joined",
        order_by="Ingredient.order_id"
    )

    def __repr__(self):
        return f"<Direction {self.recipe_id} {self.order_id}>"

class Ingredient(db.Model):
    __tablename__ = "ingredient"
    id = db.Column(db.Integer, primary_key=True)
    direction_id = db.Column(db.Integer, db.ForeignKey("direction.id"),
                          nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Float)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"))
    item = db.Column(db.String, nullable=False)

    unit = db.relationship(
        Unit,
        lazy="joined",
    )

    def __repr__(self):
        return f"<Ingredient {self.item}>"