from datetime import datetime
# from marshmallow_sqlalchemy import fields
from config import db, ma


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


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)


recipe_tag = db.Table(
    "recipe_tag",
    db.Column("recipe_id", db.ForeignKey(Recipe.id), primary_key=True),
    db.Column("tag_id", db.ForeignKey(Tag.id), primary_key=True),
)

class Unit(db.Model):
    __tablename__ = "unit"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Ingredient(db.Model):
    __tablename__ = "ingredient"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"),
                          nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"),
                        nullable=False)
    item = db.Column(db.String, nullable=False)

class Direction(db.Model):
    __tablename__ = "direction"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"),
                          nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)

complementary_dish = db.Table(
    "complementary_dish",
    db.Column("recipe_id", db.ForeignKey(Recipe.id), primary_key=True),
    db.Column("comp_recipe_id", db.ForeignKey(Recipe.id), primary_key=True),
)
