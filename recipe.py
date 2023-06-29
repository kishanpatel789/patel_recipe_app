from flask import abort, make_response

from config import db
from models import Recipe, recipes_schema


def read_all():
    recipes = Recipe.query.all()
    return recipes_schema.dump(recipes)