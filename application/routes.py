from flask import render_template, make_response, abort, \
    redirect, url_for, flash
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
@app.route('/tag', methods=['GET', 'POST'])
def show_tags():
    # query database
    tags = db.session.execute(
        db.select(Tag)
    ).scalars().all()

    # prepare/process form
    form = TagForm()
    if form.validate_on_submit():
        new_tag_name = form.name.data

        existing_tag = db.session.execute(
            db.select(Tag).where(Tag.name==new_tag_name)
        ).scalars().one_or_none()
        
        if existing_tag:
            flash(f"Tag '{new_tag_name}' already exists", "error")
            return redirect(url_for("show_tags"))
        else:
            new_tag = Tag(name=form.name.data)
            db.session.add(new_tag)
            db.session.commit()

            return redirect(url_for("show_tags"))

    return render_template(
        'tag.html', 
        tags=tags, 
        form=form,
    )

@app.route('/tag/new', methods=['GET', 'POST'])
def create_tag():
    form = TagForm()
    if form.validate_on_submit():
        new_tag_name = form.name.data

        existing_tag = db.session.execute(
            db.select(Tag).where(Tag.name==new_tag_name)
        ).scalars().one_or_none()
        
        if existing_tag:
            return f"Tag '{new_tag_name}' already exists"
        else:
            new_tag = Tag(name=form.name.data)
            db.session.add(new_tag)
            db.session.commit()

            return redirect(url_for("show_tags"))
        
    return render_template(
        "create_tag.html",
        form=form,
    )

@app.route('/tag/edit/<int:tag_id>', methods=['GET', 'POST'])
def edit_tag(tag_id):
    # look up tag_id
    existing_tag = db.session.execute(
        db.select(Tag).where(Tag.id==tag_id)
    ).scalars().one_or_none()

    if not existing_tag:
        abort(404)

    # populate form with existing info (GET) or get submitted form info (POST)
    form = TagForm(obj=existing_tag) # only uses obj if post request not supplied
    
    # execute form logic for POST
    if form.validate_on_submit():
        if existing_tag:
            form.populate_obj(existing_tag)
            db.session.merge(existing_tag)
            db.session.commit()      
            return redirect(url_for("show_tags"))

    return render_template(
        "edit_tag.html",
        form=form,
    )


@app.route('/tag/delete/<int:tag_id>', methods=['GET'])
def delete_tag(tag_id):
    existing_tag = db.session.execute(
        db.select(Tag).where(Tag.id==tag_id)
    ).scalars().one_or_none()

    if existing_tag:
        db.session.delete(existing_tag)
        db.session.commit()
    else:
        flash(f"Tag with ID '{tag_id}' does not exist", "error")

    return redirect(url_for("show_tags"))

    
    


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404