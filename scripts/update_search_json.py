# %%
import sys
sys.path.insert(1, '..')

from application import create_app
from application.models import db, Recipe
import json

# %%
app = create_app()

# %%
search_lib = []

with app.app_context():
    recipes = db.session.execute(
        db.select(Recipe).order_by(Recipe.name)
    ).scalars().all()

    for r in recipes:
        dict_recipe = {
            'id': r.id,
            'name': r.name,
            'tags': []
        }
        for t in r.tags:
            dict_recipe['tags'].append(f"#{t.name}")

        search_lib.append(dict_recipe)
# %%
with open('test.json', 'w') as f:
    json.dump(search_lib, f)
# %%
