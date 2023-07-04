from flask import abort, make_response

from config import db
from models import Recipe, recipes_schema, recipe_schema


def read_all():
    recipes = Recipe.query.all()
    return recipes_schema.dump(recipes)

def read_one(recipe_id):
    recipe = db.session.execute(
        db.select(Recipe).filter(
            Recipe.id==recipe_id
        )
    ).scalars().unique().one_or_none()

    if recipe is not None:
        return recipe_schema.dump(recipe)
    else:
        abort(404, f"Recipe {recipe_id} not found")

def create(recipe):
    name = recipe.get("name")
    existing_recipe = db.session.execute(
        db.select(Recipe).filter(
            Recipe.name==name
        )
    ).scalars().unique().one_or_none()
    
    if existing_recipe is None:
        new_recipe = recipe_schema.load(recipe, session=db.session)
        db.session.add(new_recipe)
        db.session.commit()
        return recipe_schema.dump(new_recipe), 201
    else:
        abort(406, f"Recipe with name {name} already exists")
