# %%

from application import create_app
from application.models import db, Recipe, Ingredient, Direction, Unit

# %%
app = create_app()

# %%
with app.app_context():
    rep = db.session.execute(
        db.select(Recipe).where(Recipe.id==1)
    ).scalars().unique().one_or_none()

    ingredients = db.session.execute(
        db.select(Ingredient).join(Ingredient.unit).where(Ingredient.recipe_id==1)
    ).scalars().unique().all()

# %%
