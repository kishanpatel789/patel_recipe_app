# %%
import sys
sys.path.insert(1, '..')

from application import create_app
from application.models import db, Recipe, Ingredient, Direction, Unit, Tag

# %%
app = create_app()

# %%
with app.app_context():
    rep = db.session.execute(
        db.select(Recipe).where(Recipe.id==2)
    ).scalars().unique().one_or_none()
    # db.session.delete(rep)
    existing_dirs = {d.order_id for d in rep.directions}

    # comp = rep.complementary_dishes.all()

    # ingredients = db.session.execute(
    #     db.select(Ingredient).where(Ingredient.recipe_id==1)
    # ).scalars().unique().all()

    # new_tag = Tag(name='hello')
    # t1 = db.session.add(new_tag)
    # t2 = db.session.commit()

    # units = db.session.execute(
    #         db.select(Unit).order_by(Unit.name)
    #     ).scalars().all()
    
    # directions = db.session.execute(
    #     db.select(Direction).where(Direction.recipe_id==2)
    # ).scalars().unique().all()

    # direction = db.session.execute(
    #     db.select(Direction).where(Direction.id==13)
    # ).scalars().unique().one_or_none()
    # db.session.delete(direction)

    # db.session.commit()

# %%
