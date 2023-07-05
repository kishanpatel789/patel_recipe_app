from flask import render_template, make_response, abort
from flask import current_app as app

from .models import db, Recipe, Ingredient, Direction


@app.route("/")
def home():
    recipes = db.session.execute(
        db.select(Recipe)
    ).scalars().unique().all()
    
    return render_template("index.html", recipes=recipes)



@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def show_recipe(recipe_id):
    # query database
    recipe = db.session.execute(
        db.select(Recipe).where(Recipe.id==recipe_id)
    ).scalars().unique().one_or_none()

    ingredients = db.session.execute(
        db.select(Ingredient).where(Ingredient.recipe_id==recipe_id)
    ).scalars().unique().all()

    directions = db.session.execute(
        db.select(Direction).where(Direction.recipe_id==recipe_id)
    ).scalars().unique().all()

    if recipe:
        return render_template(
            'recipe.html', 
            recipe=recipe, 
            ingredients=ingredients, 
            directions=directions,
        )
    else:
        abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404