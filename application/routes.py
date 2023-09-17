from flask import render_template, make_response, abort, \
    redirect, url_for, flash, request
from flask import current_app as app
import json

from .models import db, Recipe, Ingredient, Direction, Tag, Unit
from .forms import TagForm, UnitForm, RecipeForm, IngredientForm

# register custom jinja filters
def format_number(value):
    if isinstance(value, float):
        if int(value) == value:
            return int(value)
    return value
app.jinja_env.filters['format_number'] = format_number

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

    # ingredients = db.session.execute(
    #     db.select(Ingredient).where(Ingredient.recipe_id==recipe_id)
    # ).scalars().unique().all()

    # directions = db.session.execute(
    #     db.select(Direction).where(Direction.recipe_id==recipe_id)
    # ).scalars().unique().all()

    if recipe:
        return render_template(
            'recipe.html', 
            recipe=recipe, 
            # ingredients=ingredients, 
            # directions=directions,
        )
    else:
        abort(404)

@app.route('/recipe/new', methods=['GET', 'POST'])
def create_recipe():

    form = RecipeForm()
    form_ingredient_template = IngredientForm()

    # generate at least one ingredient for the first direction
    if request.method == 'GET':
        form.directions[0].ingredients.append_entry()

    # dynamically determine unit options
    units = db.session.execute(
        db.select(Unit).order_by(Unit.name)
    ).scalars().all()
    for d in form.directions:
        if d.ingredients:
            for i in d.ingredients:
                i.unit_id.choices = [(-1, '')] + [(u.id, u.name) for u in units]

    form_ingredient_template.unit_id.choices = [(-1, '')] + [(u.id, u.name) for u in units]
    
    if form.validate_on_submit():
        # check for existing recipe with name
        existing_recipe = db.session.execute(
            db.select(Recipe).where(Recipe.name==form.name.data)
        ).scalars().unique().one_or_none()

        if existing_recipe:
            flash(f"Recipe with '{form.name.data}' already exists")
            return render_template(
                    'create_recipe.html',
                    form=form,
                    form_ingredient_template=form_ingredient_template,
                )   
        else:
            try: 
                db.session.close()  # close session to handle transactional-level management
                with db.session.begin():
                    # update recipe model
                    recipe_orm = Recipe(
                        name=form.name.data,
                        created_by = 1  # TEMP UPDATE with kishan; re-do later with logged in user
                    )
                    db.session.add(recipe_orm)
                    db.session.flush()

                    # update direction model
                    for i, direction in enumerate(form.directions):
                        direction_orm = Direction(
                            recipe_id = recipe_orm.id,
                            order_id = i+1,
                            description_ = direction.description_.data,
                        )
                        db.session.add(direction_orm)
                        db.session.flush()

                        # update ingredient model
                        for j, ingredient in enumerate(direction.ingredients):
                            ingredient_orm = Ingredient(
                                direction_id = direction_orm.id,
                                order_id = j+1,
                                quantity = ingredient.quantity.data,
                                unit_id = ingredient.unit_id.data,
                                item = ingredient.item.data,
                            )
                            db.session.add(ingredient_orm)

            except Exception as e:
                flash(f"An error occurred: {e}")
                return render_template(
                    'create_recipe.html',
                    form=form,
                    form_ingredient_template=form_ingredient_template,
                )

        return redirect(url_for('home'))
    
    if request.method == 'POST' and form.errors:
        for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", "error")

    # if request.method == 'POST':
    #     return form.data
    return render_template(
        'create_recipe.html',
        form=form,
        form_ingredient_template=form_ingredient_template,
        header='New Recipe',
    )

@app.route('/recipe/edit/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):

    # look up recipe_id
    existing_recipe = db.session.execute(
        db.select(Recipe).where(Recipe.id==recipe_id)
    ).scalars().one_or_none()

    if not existing_recipe:
        flash(f"Recipe with ID '{recipe_id}' does not exist and cannot be edited", "error")
        return redirect(url_for('home'))
    else:
        # populate form with submitted form info or with existing info
        form = RecipeForm(obj=existing_recipe)

        # dynamically determine unit options
        units = db.session.execute(
            db.select(Unit).order_by(Unit.name)
        ).scalars().all()
        for d in form.directions:
            if d.ingredients:
                for i in d.ingredients:
                    i.unit_id.choices = [(-1, '')] + [(u.id, u.name) for u in units]

        # # TEST POST INPUT
        # if request.method == 'POST':
        #     return form.data

        # persist form content 
        if form.validate_on_submit():
            # update recipe model
            existing_recipe.name = form.name.data
            existing_recipe.modified_by = 2

            # update direction model - create, update, delete
            # existing_direction_order_ids = {d.order_id for d in existing_recipe.directions}
            existing_direction_cnt = len(existing_recipe.directions)
            new_directions = []
            for form_direction_index, form_direction in enumerate(form.directions):
                if form_direction_index < existing_direction_cnt:
                    # update
                    existing_direction = existing_recipe.directions[form_direction_index]
                    existing_direction.description_ = form_direction.description_
                else:
                    # create
                    pass

            # delete

            # update ingredient model - create, update, delete

            # form.populate_obj(existing_recipe)
            db.session.commit()      
            return redirect(url_for("home"))

        if request.method == 'POST' and form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", "error")

        

        # set template form
        form_ingredient_template = IngredientForm()
        form_ingredient_template.unit_id.choices = [(-1, '')] + [(u.id, u.name) for u in units]

        return render_template(
            'create_recipe.html',
            form=form,
            form_ingredient_template=form_ingredient_template,
            header='Edit Recipe',
        )
    


    # if form.validate_on_submit():
    #     # check for existing recipe with name
    #     existing_recipe = db.session.execute(
    #         db.select(Recipe).where(Recipe.name==form.name.data)
    #     ).scalars().unique().one_or_none()

    #     if existing_recipe:
    #         flash(f"Recipe with '{form.name.data}' already exists")
    #         return render_template(
    #                 'create_recipe.html',
    #                 form=form,
    #                 form_ingredient_template=form_ingredient_template,
    #             )   
    #     else:
    #         try: 
    #             db.session.close()  # close session to handle transactional-level management
    #             with db.session.begin():
    #                 # update recipe model
    #                 recipe_orm = Recipe(
    #                     name=form.name.data,
    #                     created_by = 1  # TEMP UPDATE with kishan; re-do later with logged in user
    #                 )
    #                 db.session.add(recipe_orm)
    #                 db.session.flush()

    #                 # update direction model
    #                 for i, direction in enumerate(form.directions):
    #                     direction_orm = Direction(
    #                         recipe_id = recipe_orm.id,
    #                         order_id = i+1,
    #                         description = direction.description_.data,
    #                     )
    #                     db.session.add(direction_orm)
    #                     db.session.flush()

    #                     # update ingredient model
    #                     for j, ingredient in enumerate(direction.ingredients):
    #                         ingredient_orm = Ingredient(
    #                             direction_id = direction_orm.id,
    #                             order_id = j+1,
    #                             quantity = ingredient.quantity.data,
    #                             unit_id = ingredient.unit_id.data,
    #                             item = ingredient.item.data,
    #                         )
    #                         db.session.add(ingredient_orm)

    #         except Exception as e:
    #             flash(f"An error occurred: {e}")
    #             return render_template(
    #                 'create_recipe.html',
    #                 form=form,
    #                 form_ingredient_template=form_ingredient_template,
    #             )

    #     return redirect(url_for('home'))
    
    # if request.method == 'POST' and form.errors:
    #     for field, errors in form.errors.items():
    #             for error in errors:
    #                 flash(f"{field}: {error}", "error")

    # # if request.method == 'POST':
    # #     return form.data
    # return render_template(
    #     'create_recipe.html',
    #     form=form,
    #     form_ingredient_template=form_ingredient_template,
    #     header='Edit Recipe',
    # )


# tag
@app.route('/tag', methods=['GET'])
def show_tags():
    # query database
    tags = db.session.execute(
        db.select(Tag)
    ).scalars().all()

    # prepare/process form
    form = TagForm()

    return render_template(
        'tag.html', 
        tags=tags, 
        form=form,
    )

@app.route('/tag/new', methods=['POST'])
def create_tag():
    form = TagForm()

    if form.validate_on_submit():
        new_tag_name = form.name.data

        # look for existing tag with name
        existing_tag = db.session.execute(
            db.select(Tag).where(Tag.name==new_tag_name)
        ).scalars().one_or_none()
        
        if existing_tag:
            flash(f"Tag '{new_tag_name}' already exists", "error")
        else:
            new_tag = Tag()
            form.populate_obj(new_tag)
            db.session.add(new_tag)
            db.session.commit()
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "error")

    return redirect(url_for("show_tags"))
        
@app.route('/tag/edit/<int:tag_id>', methods=['POST'])
def edit_tag(tag_id):
    # look up tag_id
    existing_tag = db.session.execute(
        db.select(Tag).where(Tag.id==tag_id)
    ).scalars().one_or_none()

    if not existing_tag:
        flash(f"Tag with ID '{tag_id}' does not exist", "error")
    else:
        # populate form submitted form info or with existing info
        form = TagForm(obj=existing_tag) 
        
        # store form content 
        if form.validate_on_submit():
            if existing_tag:
                form.populate_obj(existing_tag)
                db.session.commit()      
    return redirect(url_for("show_tags"))


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

# unit
@app.route('/unit', methods=['GET'])
def show_units():
    # query database
    units = db.session.execute(
        db.select(Unit)
    ).scalars().all()

    form = UnitForm()

    return render_template(
        'unit.html', 
        units=units, 
        form=form,
        default='',
    )

@app.route('/unit/new', methods=['POST'])
def create_unit():
    form = UnitForm()

    if form.validate_on_submit():
        new_unit_name = form.name.data

        # look for existing unit with name
        existing_unit = db.session.execute(
            db.select(Unit).where(Unit.name==new_unit_name)
        ).scalars().one_or_none()
        
        if existing_unit:
            flash(f"Unit '{new_unit_name}' already exists", "error")
        else:
            new_unit = Unit()
            form.populate_obj(new_unit)
            db.session.add(new_unit)
            db.session.commit()
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "error")

    return redirect(url_for("show_units"))

@app.route('/unit/edit/<int:unit_id>', methods=['POST'])
def edit_unit(unit_id):
    # look up unit_id
    existing_unit = db.session.execute(
        db.select(Unit).where(Unit.id==unit_id)
    ).scalars().one_or_none()

    if not existing_unit:
        flash(f"Unit with ID '{unit_id}' does not exist", "error")
    else:
        # populate form submitted form info or with existing info
        form = UnitForm(obj=existing_unit) 

        # store form content
        if form.validate_on_submit():
            form.populate_obj(existing_unit)
            db.session.commit()      
    return redirect(url_for("show_units"))

@app.route('/unit/delete/<int:unit_id>', methods=['GET'])
def delete_unit(unit_id):
    existing_unit = db.session.execute(
        db.select(Unit).where(Unit.id==unit_id)
    ).scalars().one_or_none()

    if existing_unit:
        db.session.delete(existing_unit)
        db.session.commit()
    else:
        flash(f"Unit with ID '{unit_id}' does not exist", "error")

    return redirect(url_for("show_units"))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404