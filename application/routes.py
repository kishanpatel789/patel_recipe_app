from flask import render_template, make_response
from flask import current_app as app

from .models import db, Recipe


@app.route("/")
def home():
    recipes = db.session.execute(
        db.select(Recipe)
    ).scalars().unique().all()
    
    return render_template("index.html", recipes=recipes)



@app.route("/{int:recipe_id}")
def show_recipe(recipe_id):
    recipe = db.session.execute(
        db.select(Recipe)
    ).scalars().unique().all()

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404