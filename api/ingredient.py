from flask import abort, make_response

from config import db
from models import Ingredient, ingredients_schema, ingredient_schema


def read_all(recipe_id):
    ingredients = db.session.execute(
        db.select(Ingredient).filter(
            Ingredient.recipe_id==recipe_id
        )
    ).scalars().unique().all()

    return ingredients_schema.dump(ingredients)

def read_one(ingredient_id):
    ingredient = db.session.execute(
        db.select(Ingredient).filter(
            Ingredient.id==ingredient_id
        )
    ).scalars().unique().one_or_none()

    if ingredient is not None:
        return ingredient_schema.dump(ingredient)
    else:
        abort(404, f"Ingredient {ingredient_id} not found")
