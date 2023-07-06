from flask import render_template, make_response, abort, redirect, url_for
from flask import current_app as app

from .models import db, Recipe, Ingredient, Direction, Tag
from .forms import TagForm


@app.route("/")
def home():
    recipes = db.session.execute(
        db.select(Recipe)
    ).scalars().unique().all()
    
    return render_template("index.html", recipes=recipes)

# recipe
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

# tag
@app.route('/tag', methods=['GET'])
def show_tags():
    # query database
    tags = db.session.execute(
        db.select(Tag)
    ).scalars().all()

    return render_template(
        'tag.html', 
        tags=tags, 
    )

@app.route('/new-tag', methods=['GET', 'POST'])
def create_tag():
    form = TagForm()
    if form.validate_on_submit():
        return redirect(url_for("show_tags"))
    return render_template(
        "create_tag.html",
        form=form,
    )



@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404