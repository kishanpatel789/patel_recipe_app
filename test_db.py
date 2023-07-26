# %%

from application import create_app
from application.models import db, Recipe, Ingredient, Direction, Unit, Tag

# %%
app = create_app()

# %%
with app.app_context():
    # rep = db.session.execute(
    #     db.select(Recipe).where(Recipe.id==1)
    # ).scalars().unique().one_or_none()

    # comp = rep.complementary_dishes.all()

    # ingredients = db.session.execute(
    #     db.select(Ingredient).where(Ingredient.recipe_id==1)
    # ).scalars().unique().all()

    # new_tag = Tag(name='hello')
    # t1 = db.session.add(new_tag)
    # t2 = db.session.commit()

    units = db.session.execute(
            db.select(Unit).order_by(Unit.name)
        ).scalars().all()

# %%
