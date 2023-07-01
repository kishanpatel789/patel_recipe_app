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
