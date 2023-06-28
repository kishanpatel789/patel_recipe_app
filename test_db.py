# %%

from config import app, db
from models import User, Recipe, Tag, recipe_tag

# %%
with app.app_context():
    tt = db.session.execute(
        db.select(Recipe)
    ).scalars().unique().all()

# %%
